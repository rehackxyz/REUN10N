# crypto - misdirection

```
```
Flag:`lactf{d0nt_b3_n0nc00p3r4t1v3_w1th_my_s3rv3r}`

Solved by Ha1qal
#!/usr/bin/env python3
import time
import threading
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter

BASE = "https://misdirection-i1539.instancer.lac.tf"

# Bootstrap needs replies (slow crypto)
BOOT_TIMEOUT  = (5, 180)   # (connect, read)
RESET_TIMEOUT = (5, 240)

# Race is fire-and-forget (we don't need replies)
RACE_TIMEOUT  = (2, 0.8)   # short read timeout on purpose

GOAL = 14
ATTEMPTS = 12

# Start here (don’t go crazy; too high can make the instance crawl)
START_WORKERS = 220
MAX_WORKERS   = 420

thread_local = threading.local()

def get_session() -> requests.Session:
    """Thread-local Session: thread-safe + reuses keep-alive per thread."""
    s = getattr(thread_local, "session", None)
    if s is None:
        s = requests.Session()
        s.headers.update({"Content-Type": "application/json"})
        # Bigger pool helps under concurrency
        adapter = HTTPAdapter(pool_connections=256, pool_maxsize=256, max_retries=0)
        s.mount("https://", adapter)
        s.mount("http://", adapter)
        thread_local.session = s
    return s

def get_json(path: str, timeout=BOOT_TIMEOUT):
    r = requests.get(BASE + path, timeout=timeout)
    r.raise_for_status()
    return r.json()

def post_json(path: str, data, timeout=BOOT_TIMEOUT):
    r = requests.post(BASE + path, json=data, timeout=timeout)
    r.raise_for_status()
    return r.json()

def wait_ready(max_s=180):
    t0 = time.time()
    while time.time() - t0 < max_s:
        try:
            if get_json("/status", timeout=(3, 10)).get("status") is True:
                return
        except Exception:
            pass
        time.sleep(0.2)
    raise RuntimeError("Instance not ready")

def reset_instance():
    try:
        get_json("/regenerate-keys", timeout=RESET_TIMEOUT)
    except Exception:
        # even if we timeout, server may still be resetting
        pass

    wait_ready()

    # wait for count to be stably 0 (avoid leftover in-flight /grow)
    stable = 0
    last = None
    for _ in range(30):
        try:
            c = get_json("/current-count", timeout=(3, 15))["count"]
        except Exception:
            c = None
        if c == 0 and c == last:
            stable += 1
            if stable >= 3:
                return
        else:
            stable = 0
        last = c
        time.sleep(0.25)

def munge_header(sig: str, tag: str) -> str:
    """
    IMPORTANT: only change the first line.
    The server's import_signature() skips header content until first '\\n',
    so this does NOT change the signature meaning — but it DOES avoid cache hits.
    """
    lines = sig.split("\n")
    lines[0] = f"X{tag}"
    return "\n".join(lines)

def bootstrap_to_3():
    """Grow 0->1->2->3 normally (needs responses). Returns signature for count=3."""
    wait_ready()
    sig = get_json("/zero-signature")["signature"]
    count = 0

    while count < 3:
        j = post_json("/grow", {"count": count, "sig": sig}, timeout=BOOT_TIMEOUT)
        if j.get("signature") == "null":
            raise RuntimeError(f"Bootstrap grow rejected: {j}")
        count = j["count"]
        sig = j["signature"]

    return count, sig  # (3, sig_for_3)

def barrier_burst(count: int, sig_for_count: str, workers: int):
    """
    True concurrent burst WITHOUT TLS stampede:
    - Each thread uses its own persistent Session (keep-alive)
    - Each thread does a tiny warm-up GET before waiting on the barrier
    - Then all threads POST /grow at once
    """
    barrier = threading.Barrier(workers + 1)

    def fire(i: int):
        s = get_session()
        try:
            # Warm-up so the TLS connection exists before the barrier release
            s.get(BASE + "/status", timeout=(2, 5))
        except Exception:
            pass

        # Unique header per request => avoid signature_cache fast path
        sig_i = munge_header(sig_for_count, f"{int(time.time()*1000)}-{i}")

        try:
            barrier.wait()
        except Exception:
            return

        try:
            s.post(
                BASE + "/grow",
                json={"count": count, "sig": sig_i},
                timeout=RACE_TIMEOUT,
            )
        except Exception:
            pass

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(fire, i) for i in range(workers)]
        # Release everyone
        barrier.wait()
        # Drain
        for _ in as_completed(futs):
            pass

def poll_until_done(goal=GOAL, max_wait=50, interval=1.0, stable_for=7.0):
    """
    Wait for late increments:
    - returns (hit_goal, last_count, max_seen)
    - stops early if goal reached
    - otherwise stops when count doesn't change for stable_for seconds
    """
    t0 = time.time()
    last = None
    last_change = time.time()
    max_seen = -1

    while time.time() - t0 < max_wait:
        try:
            c = get_json("/current-count", timeout=(3, 20))["count"]
        except Exception:
            time.sleep(interval)
            continue

        max_seen = max(max_seen, c)
        if c >= goal:
            return True, c, max_seen

        if last is None or c != last:
            last = c
            last_change = time.time()
        else:
            if time.time() - last_change >= stable_for:
                return False, c, max_seen

        time.sleep(interval)

    return False, last if last is not None else max_seen, max_seen

def get_flag():
    wait_ready()
    return post_json("/flag", {}, timeout=(3, 30))

def solve():
    workers = START_WORKERS

    for attempt in range(1, ATTEMPTS + 1):
        print(f"[+] Attempt {attempt}: reset -> bootstrap -> burst (workers={workers})")
        reset_instance()

        try:
            count, sig3 = bootstrap_to_3()
        except Exception as e:
            print(f"    [!] bootstrap failed: {e}")
            time.sleep(4)
            continue

        assert count == 3

        barrier_burst(3, sig3, workers=workers)

        hit, last, mx = poll_until_done(goal=GOAL, max_wait=55, interval=1.0, stable_for=8.0)
        print(f"    count stable={last} (max_seen={mx})")

        if hit:
            out = get_flag()
            print("[+] " + out["msg"])
            return

        # Don't reset immediately; let server clear backlog a bit
        time.sleep(6)

        # Smart-ish tuning:
        # - If we're stuck at 4, not enough requests are reaching before the first increment
        # - If we get close (10-13), small increases are better than huge ones
        if mx <= 4:
            workers = min(MAX_WORKERS, workers + 80)
        elif mx < 10:
            workers = min(MAX_WORKERS, workers + 40)
        else:
            workers = min(MAX_WORKERS, workers + 15)

    print("[-] No win. Try raising ATTEMPTS, or set START_WORKERS=260.")

if __name__ ==

Solved by: yappare
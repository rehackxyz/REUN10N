# crypto - The Roulette Conspiracy

```python
from pwn import remote, context
import re, random

context.log_level = "debug"   # <-- keep this until it works

HOST = "chall.0xfun.org"
PORT = 48958
XORC = 0xCAFEBABE

def recv_prompt(p):
    # Match '>' + any whitespace (space/tab/newline)
    p.recvregex(br">\s*", timeout=5)

def recv_int_line(p):
    while True:
        line = p.recvline(timeout=5)
        if not line:
            continue
        m = re.search(rb"(\d+)", line)
        if m:
            return int(m.group(1))

# --- untemper (same as before) ---
def undo_right(y, shift):
    x = y
    for _ in range(5):
        x = y ^ (x >> shift)
    return x & 0xFFFFFFFF

def undo_left(y, shift, mask):
    x = y
    for _ in range(5):
        x = y ^ ((x << shift) & mask)
    return x & 0xFFFFFFFF

def untemper(y):
    y = undo_right(y, 18)
    y = undo_left(y, 15, 0xEFC60000)
    y = undo_left(y, 7,  0x9D2C5680)
    y = undo_right(y, 11)
    return y & 0xFFFFFFFF

def main():
    p = remote(HOST, PORT)

    # Wake the service (some don't print until input)
    p.sendline(b"fd")     # any junk command is fine
    recv_prompt(p)

    raws = []
    for _ in range(624):
        p.sendline(b"spin")
        obf = recv_int_line(p)
        raws.append(obf ^ XORC)
        recv_prompt(p)

    state = [untemper(x) for x in raws]
    r = random.Random()
    r.setstate((3, tuple(state + [624]), None))

    preds = [r.getrandbits(32) for _ in range(10)]

    p.sendline(b"predict")
    p.recvregex(br"Predict next 10.*:\s*", timeout=5)
    p.sendline((" ".join(map(str, preds))).encode())

    print(p.recvall(timeout=5).decode(errors="ignore"))

if __name__ == "__main__":
    main()
```

FLAG:`0xfun{m3rs3nn3_tw1st3r_unr4v3l3d}`

Solved by: ha1qal
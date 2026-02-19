# crypto - The Slot Whisperer

```python
#!/usr/bin/env python3
from pwn import remote
import re

HOST = "chall.0xfun.org"
PORT = 42166

M = 2147483647
A = 48271
C = 12345

def recover_last_state(outputs):
    """
    outputs: list of spins where spin_i = state_i % 100 and
             state_{i+1} = (A*state_i + C) % M
    Returns list of candidate states corresponding to the LAST observed spin.
    """
    if len(outputs) < 2:
        return []

    o0, o1 = outputs[0], outputs[1]

    # Enumerate s0 ≡ o0 (mod 100), but iterate s1 cheaply by adding a constant delta
    s0 = o0
    s1 = (A * s0 + C) % M
    delta = (A * 100) % M

    cands = []
    n = (M - 1 - o0) // 100 + 1  # about 21M steps
    for _ in range(n):
        if s1 % 100 == o1:
            cands.append(s1)  # this is state_1
        s1 += delta
        if s1 >= M:
            s1 -= M

    # Filter forward for outputs[2..]
    for oi in outputs[2:]:
        new = []
        for s in cands:
            s2 = (A * s + C) % M
            if (s2 % 100) == oi:
                new.append(s2)
        cands = new
        if not cands:
            break

    return cands

def predict_next(state_last, n=5):
    out = []
    s = state_last
    for _ in range(n):
        s = (A * s + C) % M
        out.append(s % 100)
    return out

def main():
    io = remote(HOST, PORT)

    # Read until we see "Predict" (do NOT include prompt part in parsing!)
    raw = io.recvuntil(b"Predict", timeout=10)
    if b"Predict" not in raw:
        print("Did not find Predict prompt.")
        return

    prefix = raw.split(b"Predict", 1)[0]
    spins = [int(x) for x in re.findall(rb"\b\d+\b", prefix)]
    spins = [x for x in spins if 0 <= x < 100]

    if len(spins) != 10:
        print(f"Expected 10 spins, got {len(spins)}: {spins}")
        print("Raw prefix:\n", prefix.decode(errors="ignore"))
        return

    # Now read the rest of the prompt up to ':'
    io.recvuntil(b":", timeout=3)

    cands = recover_last_state(spins)
    if len(cands) != 1:
        print(f"State not unique (cands={len(cands)}). Spins={spins}")
        # If this happens, it usually means the service printed more/less than 10 spins
        return

    ans = predict_next(cands[0], 5)
    payload = " ".join(map(str, ans))
    print("[spins]", spins)
    print("[send ]", payload)

    io.sendline(payload.encode())
    print(io.recvall(timeout=3).decode(errors="ignore"))

if __name__ == "__main__":
    main()
```
FLAG:`0xfun{sl0t_wh1sp3r3r_lcg_cr4ck3d}`

Solved by: ha1qal
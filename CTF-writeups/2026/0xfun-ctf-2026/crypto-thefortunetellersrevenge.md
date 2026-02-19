# crypto - The Fortune Teller's Revenge

FLAG:`0xfun{r3v3ng3_0f_th3_f0rtun3_t3ll3r}`
#!/usr/bin/env python3
from pwn import remote
import re
import bisect

# Known constants (given)
A = 2862933555777941757
C = 3037000493
MOD = 1 << 64
MASK = MOD - 1

def lcg_step(s: int) -> int:
    return (A * s + C) & MASK

def lcg_params_k(k: int):
    """
    Return (mul, add) such that applying the LCG k times is:
        s' = mul*s + add (mod 2^64)
    Uses binary exponentiation of affine transforms.
    """
    mul, add = 1, 0           # identity
    bm, ba = A, C             # base transform
    while k > 0:
        if k & 1:
            mul = (bm * mul) & MASK
            add = (bm * add + ba) & MASK
        # square the base transform: (bm,ba) o (bm,ba)
        ba = (bm * ba + ba) & MASK
        bm = (bm * bm) & MASK
        k >>= 1
    return mul, add

def inv_affine(mul: int, add: int):
    """Inverse of s' = mul*s + add over mod 2^64 (mul must be odd)."""
    inv_mul = pow(mul, -1, MOD)
    inv_add = (-inv_mul * add) & MASK
    return inv_mul, inv_add

def recover_last_state_from_3_high32(g1: int, g2: int, g3: int, mul: int, add: int):
    """
    Observations:
        high32(s1)=g1
        s2 = mul*s1 + add
        high32(s2)=g2
        s3 = mul*s2 + add
        high32(s3)=g3
    Recover s3 (and s2,s1) using 16+16 split on low32(s1).
    """
    mul &= MASK
    add &= MASK

    # s1 = (g1<<32) | x, x is unknown low32
    base = (mul * ((g1 << 32) & MASK) + add) & MASK
    mul16 = (mul << 16) & MASK

    # Precompute v(x0) = base + mul*x0 for x0 in [0..65535]
    vals = [0] * (1 << 16)
    for x0 in range(1 << 16):
        vals[x0] = (base + (mul * x0 & MASK)) & MASK

    idx_sorted = sorted(range(1 << 16), key=vals.__getitem__)
    v_sorted = [vals[i] for i in idx_sorted]
    x0_sorted = idx_sorted  # idx is x0 itself

    L = (g2 << 32) & MASK
    R = (((g2 + 1) << 32) - 1) & MASK

    for x1 in range(1 << 16):
        term1 = (mul16 * x1) & MASK

        start = (L - term1) & MASK
        end   = (R - term1) & MASK

        if start <= end:
            ranges = [(start, end)]
        else:
            ranges = [(0, end), (start, MASK)]

        for st, en in ranges:
            i = bisect.bisect_left(v_sorted, st)
            j = bisect.bisect_right(v_sorted, en)
            for t in range(i, j):
                x0 = x0_sorted[t]
                x = x0 | (x1 << 16)
                s1 = ((g1 << 32) | x) & MASK

                s2 = (mul * s1 + add) & MASK
                if (s2 >> 32) != g2:
                    continue

                s3 = (mul * s2 + add) & MASK
                if (s3 >> 32) != g3:
                    continue

                return s3, s2, s1

    return None

def candidate_steps_likely():
    # Fast path candidates first (common CTF “pattern changed” choices)
    ms = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 13, 16, 32, 64, 128, 256, 512, 1024, 1337]
    steps = set([1, 100000, 100001, (1<<32), (1<<32)+1])
    for m in ms:
        if m > 0:
            steps.add(100000 * m)
            steps.add(100000 * m + 1)
            steps.add(100000 * m - 1)
    return sorted(s for s in steps if s > 0)

def candidate_steps_extended():
    ms = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,16,32,64,128,256,512,1024,1337,4096,8192,16384,32768,65536]
    steps = set(candidate_steps_likely())
    for m in ms:
        if m > 0:
            steps.add(100000 * m)
            steps.add(100000 * m + 1)
            steps.add(100000 * m - 1)
    steps.update([42, 69, 420, 2026, 31337, 65536])
    return sorted(s for s in steps if s > 0)

def main():
    import sys
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} HOST PORT")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    p = remote(host, port)

    # Server prints 3 integers (32-bit glimpses)
    g = []
    for _ in range(3):
        line = p.recvline().strip()
        g.append(int(line))

    # Read the prompt (contains ':')
    prompt = p.recvuntil(b":").decode(errors="ignore")
    m = re.search(r"next\s+(\d+)", prompt, re.IGNORECASE)
    k_predict = int(m.group(1)) if m else 5

    g1, g2, g3 = g
    print(f"[+] g1={g1} g2={g2} g3={g3}  (need {k_predict})")

    found = None

    # Try likely candidates, then extended
    for steps in (candidate_steps_likely(), candidate_steps_extended()):
        for k in steps:
            mul, add = lcg_params_k(k)

            # forward
            res = recover_last_state_from_3_high32(g1, g2, g3, mul, add)
            if res:
                found = ("forward", k, mul, add, res)
                break

            # backward (in case “across time itself” means reverse stepping)
            im, ia = inv_affine(mul, add)
            res = recover_last_state_from_3_high32(g1, g2, g3, im, ia)
            if res:
                found = ("backward", k, im, ia, res)
                break

        if found:
            break

    if not found:
        print("[-] Could not match any candidate stride.")
        print("    If needed: add more candidates in candidate_steps_extended().")
        p.close()
        return

    direction, k, mul, add, (s3, s2, s1) = found
    print(f"[+] matched stride k={k} ({direction})")
    print(f"[+] recovered last full state s3 = {s3}")

    # Most likely the server wants the next 5 *consecutive* RNG states after s3:
    preds = []
    s = s3
    for _ in range(k_predict):
        s = lcg_step(s)
        preds.append(s)

    ans = " ".join(str(x) for x in preds)
    p.sendline(ans.encode())
    print("[+] sent predictions")
    p.interactive()

if __name__ == "__main__":
    main()

Solved by: ha1qal
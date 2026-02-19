# crypto - Bitstorm

```python
#!/usr/bin/env python3
import ast, re

MASK64 = (1 << 64) - 1
NVAR = 2048
MASKV = (1 << NVAR) - 1

def parse_outputs(path="output.txt"):
    txt = open(path, "r", encoding="utf-8").read()
    m = re.search(r"\[(.*)\]", txt, re.S)
    if not m:
        raise ValueError("Couldn't find the outputs list in output.txt")
    return ast.literal_eval("[" + m.group(1) + "]")

# --- bit-expression word ops ---
# Represent a 64-bit word as a list of 64 "expressions".
# Each expression is a Python int bitset of length 2048, indicating which seed bits XOR to it.
def shl(bits, k):
    if k == 0: return bits[:]
    return [0]*k + bits[:64-k]

def shr(bits, k):
    if k == 0: return bits[:]
    return bits[k:] + [0]*k

def rol(bits, r):
    r %= 64
    if r == 0: return bits[:]
    return bits[-r:] + bits[:-r]

def ror(bits, r):
    r %= 64
    if r == 0: return bits[:]
    return bits[r:] + bits[:r]

def xor_bits(a, b):
    return [x ^ y for x, y in zip(a, b)]

def mix_val(val_bits, i):
    mixed = xor_bits(val_bits, xor_bits(shl(val_bits, 11), shr(val_bits, 7)))
    rot = (i * 3) % 64
    return rol(mixed, rot)

def init_state_symbolic():
    # seed_int was built from 256 bytes big-endian, then split into 32x64-bit chunks:
    # state[i] = (seed_int >> (64*(31-i))) & 2^64-1
    # Word bit b corresponds to seed bit position (shift + b), where b is LSB index.
    state = []
    for i in range(32):
        shift = 64 * (31 - i)
        word = [1 << (shift + b) for b in range(64)]
        state.append(word)
    return state

def next_symbolic(state):
    taps = [0, 1, 3, 7, 13, 22, 28, 31]
    s = state

    new = [0] * 64
    for i in taps:
        new = xor_bits(new, mix_val(s[i], i))

    last = s[-1]
    new = xor_bits(new, xor_bits(shr(last, 13), shl(last, 5)))

    new_state = s[1:] + [new]

    out = [0] * 64
    for i in range(32):
        if i % 2 == 0:
            out = xor_bits(out, new_state[i])
        else:
            out = xor_bits(out, ror(new_state[i], 2))  # matches (val>>2)|(val<<62)
    return new_state, out

def build_linear_system(outputs):
    st = init_state_symbolic()
    rows = []
    for obs in outputs:
        st, out_bits = next_symbolic(st)
        for b in range(64):
            expr = out_bits[b]              # 2048-bit coeff vector (bitset)
            rhs  = (obs >> b) & 1
            rows.append(expr | (rhs << NVAR))
    return rows

def gauss_solve_gf2(rows):
    # Use "lowest-set-bit pivot" so back-substitution works descending.
    piv = {}  # col -> row

    for r in rows:
        rr = r
        while True:
            coeff = rr & MASKV
            if coeff == 0:
                if (rr >> NVAR) & 1:
                    raise ValueError("Inconsistent system (0 = 1)")
                break
            lsb = coeff & -coeff
            col = lsb.bit_length() - 1
            if col in piv:
                rr ^= piv[col]
            else:
                piv[col] = rr
                break

    if len(piv) != NVAR:
        raise ValueError(f"Not full rank: rank={len(piv)} vars={NVAR}")

    sol = 0
    for col in sorted(piv.keys(), reverse=True):
        row = piv[col]
        coeff = row & MASKV
        rhs = (row >> NVAR) & 1
        coeff_wo = coeff ^ (1 << col)
        parity = ((coeff_wo & sol).bit_count() & 1)
        bit = rhs ^ parity
        if bit:
            sol |= (1 << col)
    return sol

def main():
    outs = parse_outputs("output.txt")
    rows = build_linear_system(outs)
    sol_bits = gauss_solve_gf2(rows)

    seed_int = sol_bits
    seed_bytes = seed_int.to_bytes(256, "big")
    content = seed_bytes.split(b"\0", 1)[0]          # remove padding
    flag = b"0xfun{" + content + b"}"
    print(flag.decode("ascii"))

if __name__ == "__main__":
    main()
```
FLAG:`0xfun{L1n34r_4lg3br4_W1th_Z3_1s_Aw3s0m3}`

Solved by: ha1qal
```python
import math

with open("encrypted", "rb") as f:
    data = f.read()

ss = int.from_bytes(data, "big")

# Convert to base-9 digits
digits = []
x = ss
while x > 0:
    digits.append(x % 9)
    x //= 9
digits = digits[::-1]

o = (
    (6, 0, 7),
    (8, 2, 1),
    (5, 4, 3)
)

# Build inverse map: digit -> (q,r)
inv = {}
for a in range(3):
    for b in range(3):
        inv[o[a][b]] = (a, b)

# Each digit gives one (q,r)
pairs = [inv[d] for d in digits]

# Reconstruct trits outside → inside
L = 2 * len(pairs)  # total trits
trits = [None] * L

left = 0
right = L - 1

for q, r in pairs:
    trits[left] = q
    trits[right] = r
    left += 1
    right -= 1

# Convert base-3 trits → integer
s = 0
for t in trits:
    s = s * 3 + t

# Convert integer → bytes
flag_bytes = s.to_bytes((s.bit_length() + 7) // 8, "big")

# Print result
print(flag_bytes.decode(errors="ignore"))
```
Flag: pctf{a_l3ss_cr4zy_tr1tw1s3_op3r4ti0n_f37d4b}

Solved by: ukyovis
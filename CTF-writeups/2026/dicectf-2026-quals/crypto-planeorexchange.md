# crypto - plane-or-exchange

```
#!/usr/bin/env python3
import hashlib
import sympy as sp

t = sp.Symbol("t")

pubA = t**14 - 11*t**13 + 61*t**12 - 217*t**11 + 548*t**10 - 1032*t**9 + 1494*t**8 - 1687*t**7 + 1494*t**6 - 1032*t**5 + 548*t**4 - 217*t**3 + 61*t**2 - 11*t + 1
pubB = 2*t**14 - 19*t**13 + 84*t**12 - 226*t**11 + 405*t**10 - 523*t**9 + 540*t**8 - 527*t**7 + 540*t**6 - 523*t**5 + 405*t**4 - 226*t**3 + 84*t**2 - 19*t + 2
P = t**6 - 5*t**5 + 13*t**4 - 17*t**3 + 13*t**2 - 5*t + 1

ciphertext = bytes.fromhex(
    "288cdf5ecf3eb860e2cb6790bff63baceaebb6ed511cd94dd0753bac59962ef0"
    "cd171231dc406ac3cdc2ff299d78390ff3"
)

privA, rem = sp.div(pubA, P)
assert rem == 0

shared = sp.expand(privA * pubB)
shared_hex = hashlib.sha256(str(shared).encode()).hexdigest()

key = bytes.fromhex(shared_hex)
while len(key) < len(ciphertext):
    key += hashlib.sha256(key).digest()

pt = bytes(c ^ k for c, k in zip(ciphertext, key))
print(pt.decode())
```
Flag:`dice{plane_or_planar_my_w0rds_4r3_411_knotted_up}`

Compiled by: yappare
Solved by: g10d
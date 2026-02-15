# crypto - Curve Ball

```
$ nc curve.ctf.pascalctf.it 5004

Curve Ball
y^2 = x^3 + 1 (mod 1844669347765474229)
n = 1844669347765474230
G = (27, 728430165157041631)
Q = (1654607498571766855, 1502089065465742353)
```
You need to calculate the secret for the current Q

```
# 1. Setup the curve
p = 1844669347765474229
E = EllipticCurve(GF(p), [0, 1])

# 2. Define the points
G = E(27, 728430165157041631)
# UPDATED Q from your latest terminal output:
Q = E(1654607498571766855, 1502089065465742353)

# 3. Solve for the NEW secret
from sage.groups.generic import discrete_log
print("Calculating NEW discrete log...")
secret = discrete_log(Q, G, operation='+')

print(f"Decimal: {secret}")
print(f"Hex: {hex(secret)}")
```
Flag:`pascalCTF{sm00th_0rd3rs_m4k3_3cc_n0t_s0_h4rd_4ft3r_4ll}`

SOLVED by Ha1qal

Solved by: yappare
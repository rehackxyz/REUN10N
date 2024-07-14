# Efficient RSA
Solved by **okay**

## Question
I have heard that the smaller, the more efficient (pun intended). But how well does that apply to Cryptography?

## Solution
```
from sympy import gcd, mod_inverse

n = 13118792276839518668140934709605545144220967849048660605948916761813
e = 65537
ciphertext = 8124539402402728939748410245171419973083725701687225219471449051618

p = 3058290486427196148217508840815579
q = 4289583456856434512648292419762447

assert n == p * q, "n is not equal to p * q"

phi_n = (p - 1) * (q - 1)

d = mod_inverse(e, phi_n)

plaintext = pow(ciphertext, d, n)

flag = plaintext.to_bytes((plaintext.bit_length() + 7) // 8, byteorder='big')

print(flag.decode())
```

### Flag
`OSCTF{F4ct0r1Ng_F0r_L1f3}`

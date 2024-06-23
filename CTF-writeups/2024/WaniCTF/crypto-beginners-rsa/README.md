# Crypto - beginners_rsa
Solved by **SungJinwoo**

## Question
Do you know RSA?

## Solution
```
from sympy.ntheory import factorint
from Crypto.Util.number import long_to_bytes

# Given values
n = 317903423385943473062528814030345176720578295695512495346444822768171649361480819163749494400347
e = 65537
enc = 127075137729897107295787718796341877071536678034322988535029776806418266591167534816788125330265

# Factorize n to get the prime factors
factors = factorint(n)
assert len(factors) == 5, "Expected 5 prime factors"
p, q, r, s, a = factors.keys()

# Compute φ(n)
phi_n = (p-1) * (q-1) * (r-1) * (s-1) * (a-1)

# Compute the private exponent d
d = pow(e, -1, phi_n)

# Decrypt the ciphertext
m = pow(enc, d, n)

# Convert the decrypted message back to bytes
flag = long_to_bytes(m)
print(flag)
```

### Flag
`FLAG{S0_3a5y_1254!!}`

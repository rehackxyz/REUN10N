# Robin Mystery
Solved by: @hikki

### Question:
Robin's friend used an unusual RSA setup, and now he can't decrypt his own message! Can you step in and use a special technique to recover the plaintext ?

### Solution:
With using a method to recover plaintexts when bad RSA keys were used. Here is the resource article: https://medium.com/@g2f1/bad-rsa-keys-3157bc57528e

The solution script:
```python
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes
from math import gcd
from gmpy2 import isqrt


pem_key = """-----BEGIN PUBLIC KEY-----
MIGcMA0GCSqGSIb3DQEBAQUAA4GKADCBhgKBgGjpRi/Hr5oN5NS219dZrq6nW7AC
Y7fUItXAvbgy0TtagVKO2goQiOssL331b7zRjMvdHkEBR4bTd+hHblmynO+2//fz
4DmVgdgMnrP54+2RSzguEGS1ONX4MpJonBsEGGc1IOiKECiwIbl4DkyTxl6AnFsz
ZI2E+lLDZnX5P44FAgEQ
-----END PUBLIC KEY-----"""

rsa_key = RSA.import_key(pem_key)

n = rsa_key.n
e = rsa_key.e
cipher =  ...
c = bytes_to_long(cipher)

print(f"n: {n}")
print(f"e: {e}")

a = isqrt(n) + 1
b2 = a*a - n
while not isqrt(b2)**2 == b2:
    a += 1
    b2 = a*a - n

b = isqrt(b2)
p = a - b
q = a + b

print(f"p: {p}")
print(f"q: {q}")

def find_roots_of_unity(n, e, max_roots=10):
    phi_n = (p-1)*(q-1)  
    k = gcd(e, phi_n) 
    
    if k == 1:
        print("No nontrivial roots exist.")
        return []

    roots = []
    for a in range(1, max_roots + 1):  
        r = pow(a, phi_n // k, n)  
        if pow(r, e, n) == 1:  
            roots.append(r)

    return roots

def recover_plaintexts(c, n, e):
    phi_n = (p-1)*(q-1)
    k = gcd(e, phi_n)

    if k == 1:
        print("No valid decryption possible.")
        return []

    d = pow(e, -1, phi_n // k)
    g = pow(c, d, n) 

    roots = find_roots_of_unity(n, e)
    plaintexts = [g * l % n for l in roots] 

    return plaintexts


plaintexts = recover_plaintexts(c, n, e)

for pt in plaintexts:
    try:
        decoded = long_to_bytes(pt)
        if b'FMCTF' in decoded:
            print(f"{decoded}")
    except:
        print("Failed to decode")
```

**Flag:** `FMCTF{S0lv3d_w1th_R4b1n_fx777}`

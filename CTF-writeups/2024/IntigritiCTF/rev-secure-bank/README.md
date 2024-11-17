# Secure Bank


Solved by: @OS1R1S

## Question:
Can you crack the bank?


## Solution:
```
def rol(value, shift, bits=32):
    value &= (1 << bits) - 1
    return ((value << shift) | (value >> (bits - shift))) & ((1 << bits) - 1)

def obscure_key(a1):
    a1 = (a1 ^ 0xA5A5A5A5) & 0xFFFFFFFF
    return ((4919 * rol(a1, 3)) ^ 0x5A5A5A5A) & 0xFFFFFFFF

def generate_2fa_code(a1):
    v4 = (48879 * a1) & 0xFFFFFFFF
    v3 = v4
    for i in range(10):
        v4 = obscure_key(v4)
        v3 = (((v4 >> (i % 5)) ^ (v4 << (i % 7))) + rol(v4 ^ v3, 5)) & 0xFFFFFFFF
    return v3 & 0xFFFFFF

pin = 1337
_2fa_code = generate_2fa_code(pin)
print(f"{_2fa_code}")
#Enter superadmin PIN: 1337
#Enter your 2FA code: 5670688
```

**Flag:** `INTIGRITI{pfff7_wh47_2f4?!}`

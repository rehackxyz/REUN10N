# flagwatch

Solved by: @okay

### Question
https://en.wikipedia.org/wiki/RSA_(cryptosystem)

### Solution:

```  from Crypto.Util.number import long_to_bytes

e = 65537
n = 66082519841206442253261420880518905643648844231755824847819839195516869801231
c = 19146395818313260878394498164948015155839880044374872805448779372117637653026

p = 213055785127022839309619937270901673863
q = 310165339100312907369816767764432814137

phi = (p - 1) * (q - 1)

d = pow(e, -1, phi)

m = pow(c, d, n)
decrypted_message = long_to_bytes(m)

print("Decrypted message:", decrypted_message) ```

**Flag:** `bctf{f4c70r1z3_b3773r_4d3b35e4}`

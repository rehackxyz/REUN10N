# EZ XOR
Solved by: @hikki

### Question: 
Welcome to your first crypto challenge! 🕵️‍♂️ This one is all about XOR, one of the simplest yet most widely used operations in cryptography. Can you uncover the hidden flag?

### Solution:
Here is the solution script:
```python
from pwn import *

encryptedFlag = 'a850d725cb56b0de4fcb40de72a4df56a72ec06cafa75ecb41f51c95'

cipher = bytes.fromhex(encryptedFlag)
key = b""
flag_format = b"FMCTF{"

for i in range (len(flag_format)):
    key += bytes([cipher[i] ^ flag_format[i]])

key += bytes([cipher[-1] ^ ord('}')])

flag = xor(cipher,key)
print(flag) 
```

**Flag:** `FMCTF{X0R_1S_L1K3_MAGIC_0x1}`




# Crypto - X Marked the Spot
Solved by **yappare**

## Question
A perfect first challenge for beginners. Who said pirates can't ride trains...

## Solution

```python
import hashlib
from itertools import cycle

# Given ciphertext
ct = b'\x1d\r\x1c\x12\x16\x00\x11\x1fX\x106\x1b\x17S\x1e.\x1c\x0cZ.\x11\x12^\x03\x1c;\x0b\x04\x169^\x1d]T6\x05\nU5B\x06\x00HPCGK\x0c'

# Calculate the SHA-256 hash of the ciphertext
ct_hash = hashlib.sha256(ct).hexdigest()
print("SHA-256 Hash of Ciphertext:", ct_hash)

# Length of the key
key_length = 8

# Initialize the key
key = bytearray(key_length)

# Known parts of the flag
known_prefix = b"uiuctf{"
known_suffix = b"}"

# Determine the middle part of the flag based on length
middle_length = 48 - len(known_prefix) - len(known_suffix)
middle = b"?" * middle_length

# Recover the key using the known parts of the flag
for i in range(len(known_prefix)):
    key[i % key_length] = ct[i] ^ known_prefix[i]

for i in range(len(known_suffix)):
    key[-(i % key_length) - 1] = ct[-(i + 1)] ^ known_suffix[-(i + 1)]

# Try different offsets to find the correct alignment
for offset in range(key_length):
    test_key = key[offset:] + key[:offset]
    flag = bytes(x ^ y for x, y in zip(ct, cycle(test_key)))
    if flag.startswith(known_prefix) and flag.endswith(known_suffix) and len(flag) == 48:
        print("Recovered flag with offset", offset, ":", flag.decode('utf-8', errors='ignore'))
        break
```

### Flag
uiuctf{n0t_ju5t_th3_st4rt_but_4l50_th3_3nd!!!!!}
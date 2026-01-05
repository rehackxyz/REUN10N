# Solution

```
TARGET = [
    0x60, 0x6D, 0x5D, 0x97, 0x2C, 0x04, 0xAF, 0x7C, 0xE2, 0x9E, 0x77, 0x85, 0xD1, 0x0F, 0x1D, 0x17, 
    0xD4, 0x30, 0xB7, 0x48, 0xDC, 0x48, 0x36, 0xC1, 0xCA, 0x28, 0xE1, 0x37, 0x58, 0x0F
]

XOR_KEY = [0xC7, 0x2E, 0x89, 0x51, 0xB4, 0x6D, 0x1F]
ROTATION_PATTERN = [7, 5, 3, 1, 6, 4, 2, 0]
MAGIC_SUB = 0x93
CHUNK_SIZE = 6

def rotate_left(byte, n):
    n = n % 8
    return ((byte << n) | (byte >> (8 - n))) & 0xFF

def rotate_right(byte, n):
    n = n % 8
    return ((byte >> n) | (byte << (8 - n))) & 0xFF

buffer = TARGET.copy()

for i in range(30):
    position_value = ((i * i) + i) % 256
    buffer[i] ^= position_value

for chunk_start in range(0, 30, CHUNK_SIZE):
    chunk_end = min(chunk_start + CHUNK_SIZE, 30)
    chunk = buffer[chunk_start:chunk_end]
    chunk.reverse()
    buffer[chunk_start:chunk_end] = chunk

for i in range(30):
    buffer[i] = (buffer[i] + MAGIC_SUB) & 0xFF

for i in range(0, 30, 2):
    buffer[i], buffer[i+1] = buffer[i+1], buffer[i]

for i in range(30):
    rotation = ROTATION_PATTERN[i % len(ROTATION_PATTERN)]
    buffer[i] = rotate_right(buffer[i], rotation)

for i in range(30):
    buffer[i] ^= XOR_KEY[i % len(XOR_KEY)]

flag = ''.join(chr(b) for b in buffer)
print(flag)
```

Flag: PCTF{M4ST3R_0F_TH3_S3V3N_S34S}

Solved by: amkim13

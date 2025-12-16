```
TARGET = [
    0x15, 0x5A, 0xAC, 0xF6, 0x36, 0x22, 0x3B, 0x52, 0x6C, 0x4F, 0x90, 0xD9, 0x35, 0x63, 0xF8, 0x0E,
    0x02, 0x33, 0xB0, 0xF1, 0xB7, 0x69, 0x42, 0x67, 0x25, 0xEA, 0x96, 0x63, 0x1B, 0xA7, 0x03, 0x0B
]

XOR_KEY = [0x7E, 0x33, 0x91, 0x4C, 0xA5]
ROTATION_PATTERN = [1, 3, 5, 7, 2, 4, 6]
MAGIC_SUB = 0x5D

def rotate_left(byte, n):
    n = n % 8
    return ((byte << n) | (byte >> (8 - n))) & 0xFF

def rotate_right(byte, n):
    n = n % 8
    return ((byte >> n) | (byte << (8 - n))) & 0xFF

buffer = TARGET.copy()

for i in range(32):
    position_squared = ((i * i) % 256)
    buffer[i] ^= position_squared

for chunk_start in range(0, 32, 5):
    chunk_end = min(chunk_start + 5, 32)
    chunk = buffer[chunk_start:chunk_end]
    chunk.reverse()
    buffer[chunk_start:chunk_end] = chunk

for i in range(32):
    buffer[i] = (buffer[i] + MAGIC_SUB) & 0xFF

for i in range(0, 32, 2):
    buffer[i], buffer[i+1] = buffer[i+1], buffer[i]

for i in range(32):
    rotation = ROTATION_PATTERN[i % 7]
    buffer[i] = rotate_right(buffer[i], rotation)

for i in range(32):
    buffer[i] ^= XOR_KEY[i % 5]

flag = ''.join(chr(b) for b in buffer)
print(flag)
```

Flag: PCTF{Y0U_F0UND_TH3_P1R4T3_B00TY}

Solved by: amkim13
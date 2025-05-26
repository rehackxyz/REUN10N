# Solution

The goal is to recompute that same (seed >> 21)&0xFF sequence and then XOR it back out to recover the original characters using Linear Congruential Generator (LCG)  

```
#!/usr/bin/env python3

byte_140006470 = [
    0x3A, 0x77, 0x2C, 0xA8, 0x0A, 0x82, 0xD2, 0x7F, 0x55, 0x11,
    0x40, 0xB6, 0x62, 0x64, 0x8C, 0x39, 0x4E, 0xDE, 0xCB, 0x8B,
    0x91, 0x49, 0x60, 0xA8, 0xF1, 0x2F, 0xBD, 0xE5, 0xE0, 0x7B,
    0xDB, 0xDA, 0x7B, 0xD3, 0x33, 0x04, 0x28, 0x9E
]

A = 0xCFA8C7711A026A35
B = 0x453E9537620FF1E3

SEED0 = 0xDFB432BC61353FB0

def recover_flag():
    seed = SEED0
    flag_bytes = []
    for ob in byte_140006470:
        seed = (A - B * seed) & ((1 << 64) - 1)
        derived = (seed >> 21) & 0xFF
        flag_bytes.append(ob ^ derived)

    try:
        flag = bytes(flag_bytes).decode('utf-8')
    except UnicodeDecodeError:
        flag = ''.join(f'\\x{b:02x}' for b in flag_bytes)
    return flag

if __name__ == '__main__':
    print("Flag:", recover_flag())
```  

Flag:`flag{ed817c62d7f7dcdb05c0f6e520a7069e}`

Solved by: zeqzoq

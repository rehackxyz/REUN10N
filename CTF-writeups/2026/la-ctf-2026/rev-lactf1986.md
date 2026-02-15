# rev - lactf-1986

Extract`CHALL.IMG` to get`CHALL.EXE`

```
target = [
    0xb6, 0x8c, 0x95, 0x8f, 0x9b, 0x85, 0x4c, 0x5e, 0xec, 0xb6, 0xb8, 0xc0, 0x97, 0x93, 0x0b, 0x58, 
    0x77, 0x50, 0xb0, 0x2c, 0x7e, 0x28, 0x7a, 0xf1, 0xb6, 0x04, 0xef, 0xbe, 0x5c, 0x44, 0x78, 0xe8, 
    0x99, 0x81, 0x04, 0x8f, 0x03, 0x40, 0xa7, 0x3f, 0xfa, 0xb7, 0x08, 0x01, 0x63, 0x52, 0xe3, 0xad, 
    0xd1, 0x85, 0x9f, 0x94, 0x21, 0xd5, 0x2a, 0x5c, 0x20, 0xd4, 0x31, 0x12, 0xce, 0xaa, 0x16, 0xc7, 
    0xad, 0xdf, 0x29, 0x5d, 0x72, 0xfc, 0x24, 0x90
]

def step(ax, dx):
    orig_ax = ax
    orig_dx = dx
    
    # 0xBE: Loop 3 times - shift DX:AX right by 3
    # This matches the loop at 0x71 as well
    t_ax, t_dx = ax, dx
    for _ in range(3):
        cf = t_dx & 1
        t_dx >>= 1
        t_ax = (t_ax >> 1) | (cf << 15)
    
    # 0xC4: feedback = bit0 of (AX_after_3_shifts XOR AX_before_3_shifts)
    feedback = (t_ax ^ orig_ax) & 1
    
    # 0xCD: Final state reconstruction
    # shr dx, 1; rcr ax, 1 (Shift original state once)
    cf = orig_dx & 1
    new_dx = orig_dx >> 1
    new_ax = (orig_ax >> 1) | (cf << 15)
    
    # 0xD5-0xDB: Place feedback into bit 3 of DX
    new_dx |= (feedback << 3)
    new_dx &= 0xF
    
    return new_ax, new_dx

# ---------------------------------------------------------
prefix = b"lactf{"
needed = [target[i] ^ prefix[i] for i in range(len(prefix))]

# Brute force the seed
for dx_s in range(16):
    for ax_s in range(0x10000):
        a, d = ax_s, dx_s
        match = True
        for i in range(6):
            a, d = step(a, d)
            if (a & 0xFF) != needed[i]:
                match = False
                break
        
        if match:
            # Re-generate from found seed
            res = ""
            a, d = ax_s, dx_s
            for i in range(len(target)):
                a, d = step(a, d)
                res += chr((a & 0xFF) ^ target[i])
            if all(32 <= ord(c) < 127 for c in res[:20]): # Heuristic for printable text
                print(f"Verified Flag: {res}")
                exit()
```
Flag: `lactf{3asy_3nough_7o_8rute_f0rce_bu7_n0t_ea5y_en0ugh_jus7_t0_brut3_forc3}`

SOLVED by Ha1qal

Solved by: yappare
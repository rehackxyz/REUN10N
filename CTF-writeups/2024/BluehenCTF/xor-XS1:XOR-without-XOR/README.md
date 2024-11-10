# XS1: XOR without XOR

Solved by: @OS1R1S

## Question:
This is how XOR makes me feel.

## Solution:
```
flag = 'u_cnfrj_sr_b_34}yd1tt{0upt04lbmb'

repeated_flag = flag * 32
sliced_flag = repeated_flag[::17]
final_flag = sliced_flag[:32]

for key in range(256):  # 0x00 to 0xFF
    xor_result = ''.join(chr(ord(c) ^ key) for c in final_flag)
    print(f"Key: 0x{key:02x} - Result: {xor_result}")
#ACTUAL KEY 0x00
#udctf{just_4_b4by_1ntr0_pr0bl3m}
```

**Flag:`udctf{just_4_b4by_1ntr0_pr0bl3m}`** 

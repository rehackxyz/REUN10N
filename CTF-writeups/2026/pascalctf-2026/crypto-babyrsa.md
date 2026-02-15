# crypto - baby-rsa

SOLVED by OS1RIS 

```
#!/usr/bin/env python3
import struct
import sys

def disassemble(bytecode):
    pc = 0
    while pc < len(bytecode):
        if pc + 1 > len(bytecode):
            break

        opcode = bytecode[pc]

        if opcode == 0:
            print(f"{pc:04x}: HALT")
            pc += 1
            break

        elif opcode in [1, 2, 3, 4, 6]:
            # Format: [opcode:1][addr:4][val:1]
            if pc + 6 > len(bytecode):
                break
            addr = struct.unpack('<I', bytecode[pc+1:pc+5])[0]
            val = bytecode[pc+5]

            names = {1: 'ADD', 2: 'SUB', 3: 'MOD', 4: 'MOV', 6: 'JZ'}
            name = names[opcode]

            if opcode == 6:
                print(f"{pc:04x}: {name} [mem+{addr}], offset={val}  ; if mem[{addr}]==0, skip {val} bytes")
            else:
                print(f"{pc:04x}: {name} [mem+{addr}], {val}")
            pc += 6

        elif opcode == 5:
            # Format: [opcode:1][addr:4]
            if pc + 5 > len(bytecode):
                break
            addr = struct.unpack('<I', bytecode[pc+1:pc+5])[0]
            print(f"{pc:04x}: INPUT [mem+{addr}]  ; read char to mem[{addr}]")
            pc += 5
        else:
            print(f"{pc:04x}: UNKNOWN ({opcode})")
            pc += 1

if __name__ == "__main__":
    with open("code.pascal", "rb") as f:
        code = f.read()
    disassemble(code)


"""
algorithm:
each character at index i (0-indexed)

pattern at func of executeVM()
#Even indices (0, 2, 4, n..): mem[i] = input[i] + i
#Odd indices (1, 3, 5,n...): mem[i] = input[i] - i
"""


# AT 00A
# h = "564C755C386D39586C283E577B5F3F54445B7120821B8B5080467E158A577D5A505481518C0C9444"
offset = 0x0a0278
n = 40

with open("vm", "rb") as f:
    f.seek(offset)
    b = f.read(n)

s = ''.join(chr((x - i if i % 2 == 0 else x + i) % 256) for i, x in enumerate(b))
print(f"pascalCTF{{{s}}}")
```

Flag: `⁨pascalCTF{VMs_4r3_d14bol1c4l_3n0ugh_d0nt_y0u_th1nk}`

Solved by: yappare
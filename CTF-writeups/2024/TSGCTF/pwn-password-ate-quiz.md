# Password-Ate-Quiz

Solved by: @CapangJabba

## Question:
It seems that if you enter the correct password, they will give you the flag.

## Solution:

```
from pwn import *

def con(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    elif args.GDB:
        return gdb.debug(exe, gdbscript='''
            c
            ''')
    else:
        return process(exe)


exe = './chall'
io = con()
elf = context.binary = ELF(exe, checksec = False)

context.log_level = 'info'

#---------------------------------------------------------------------

io.recvuntil(b'> ')
io.sendline(b'A'*31)
io.recvuntil(b'> ')
io.sendline(b'4')
a = io.recv(8)
# info(a)
io.recvuntil(b'> ')
io.sendline(b'5')
a += io.recv(8)
# info(a)
io.recvuntil(b'> ')
io.sendline(b'6')
a += io.recv(8)
io.recvuntil(b'> ')
io.sendline(b'7')
a += io.recv(8)
info(f'enc_pass: {a}\n')

io.recvuntil(b'> ')
io.sendline(b'8')
b = io.recv(8)
io.recvuntil(b'> ')
io.sendline(b'9')
b += io.recv(8)
io.recvuntil(b'> ')
io.sendline(b'10')
b += io.recv(8)
io.recvuntil(b'> ')
io.sendline(b'11')
b += io.recv(8)
info(f'enc_input: {b}\n')

info(f'len a: {len(a)}')
info(f'len b: {len(b)}')

result = bytes([byte ^ ord('A') for byte in b])
info(f'key: {result}')

xor_result = bytes([a_byte ^ r_byte for a_byte, r_byte in zip(a, result)])

# Print the XOR result
info(f'password: {xor_result}')


#--------------------------------------------------------------------
io.interactive()
```

**Flag:** `TSGCTF{S74ck_h45_much_1nf0m4710n_81775684690}`

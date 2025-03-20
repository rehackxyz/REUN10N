# seal-the-deal
Solved by: @w6rstaimn

### Question: 
Can you open the gate ? 
`nc seal-the-deal.fmc.tf 2003

### Solution:
Here is the solution script:
```python
from pwn import *
from Crypto.Util.number import inverse

def solve():
   
    p = remote("seal-the-deal.fmc.tf", 2003)  #
    p.recvuntil("(n,g)= ")
    n, g = eval(p.recvline().decode().strip())  

    p.recvuntil("c1 = ")
    c1 = int(p.recvline().decode().strip())

    p.recvuntil("c2 = ")
    c2 = int(p.recvline().decode().strip())

    p.recvuntil("c3 = ")
    c3 = int(p.recvline().decode().strip())

    p.recvuntil("c4 = ")
    c4 = int(p.recvline().decode().strip())

    n_sq = n * n
    c4_inv = inverse(c4, n_sq)
    encrypted_res = (c1 * c2 * c3 * c4_inv) % n_sq

    p.sendline(str(encrypted_res))
    p.interactive()

solve()
```
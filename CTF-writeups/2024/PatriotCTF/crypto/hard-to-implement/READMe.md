# Hard to Implement

Solved by: @hikki

- Category: crypto
- Description: I have a flag for you. We should talk more over my secure communications channel.

- Challenge File: cryptor.py

### Solution:

```py
from Crypto.Cipher import AES
from pwn import *
from string import printable


p = remote('chal.competitivecyber.club', 6001)
p.recvuntil(b'> ')

encrypted_length = 32
block_length = 32

def get_block(encrypted):
    new = []
    for i in range(0, len(encrypted), block_length):
        new.append(encrypted[i:i+block_length])
    return new

def encrypt(payload):
    p.sendline(payload)
    p.recvuntil(b'Response > ')
    blocks = p.recvline().strip().decode('utf-8')
    print('  '.join(get_block(blocks)))
    print('==='*5)
    p.recvuntil(b'> ')
    return blocks



flag = ''
start_length = 15

while True:
    payload = "A" * (start_length - len(flag))
    block = encrypt(payload.encode())
    start_block = block[:32]
    print("expected: ", start_block)

    for c in printable:
        print("testing: ", c)
        inp ="A" * (start_length - len(flag)) + flag + c
        print("testing: ", inp)
        result = encrypt(inp.encode())
        first_block = result[:32]
        if first_block == start_block:
            print("found: ", c)
            flag += c
            print(flag)
            break

    if flag.endswith('}'):
        print(f'{flag=}')
        break
```

**Flag:** `pctf{ab8zf58}`


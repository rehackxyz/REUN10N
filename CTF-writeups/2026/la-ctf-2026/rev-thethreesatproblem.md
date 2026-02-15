# rev - the-three-sat-problem

```
$ ./three_sat_problem
Have you solved the Three-Sat Problem?
0111111100110101110110110000010101110011110111110000100000100011111101100111011110110100011010011001011101001001011101101110001000110011111111001000011000000101001010011100000100011110110011100111011001100011110101000111101110100000000010000011001010111011011111010000011110100010100111110000111001101100101100100000110010010001111011001010001111111001000100010010000000011111001010000000011010000011100101100000101011001010110101010001111111001011101000000001100110110010011110010011101101001100001101001110010101110010100001011011001010010101101000110101100011111111100111100111111010101000101101110101111111101010101010110001011101011111010010000010010100001100110011000111011000000111111011110111100001110011101100101000101101011110010011010011111000110110101101101111001110101001000001010110101111010011010110101000110011110100101011001110101010111101111110001011000101100101110100111111110010000110001000110100100110011110110100101011110010110111100111000001011010100100001111010100011011001101110000001111110010000111110111100110010101100000110001000010101111011010110001100011010110110000010110101000001100100000010000110111101000010001111111000101111010101110101100010111010111001010000011010101010010010100111000001100001011010001111000001111010001101101110101111011010
Incredible! Let me get the flag for you...
lactf{is_the_three_body_problem_np_hard}
```

SOLVED by Zeqzoq
```
#!/usr/bin/env python3
from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG
from elftools.elf.elffile import ELFFile
import z3


INPUT_BASE = 0x15060
INPUT_LEN = 1279  # strlen must be 1279
FUNC_START = 0x1289  # sub_1289


@dataclass(frozen=True)
class Seg:
    vaddr: int
    memsz: int
    off: int
    filesz: int

    def contains(self, addr: int, size: int = 1) -> bool:
        return self.vaddr <= addr and addr + size <= self.vaddr + self.memsz

    def file_backed(self, addr: int, size: int = 1) -> bool:
        if not self.contains(addr, size):
            return False
        return addr + size <= self.vaddr + self.filesz

    def vaddr_to_off(self, addr: int) -> int:
        return self.off + (addr - self.vaddr)


def load_segs(path: str) -> Tuple[bytes, list[Seg]]:
    with open(path, "rb") as f:
        blob = f.read()
        f.seek(0)
        elf = ELFFile(f)
        segs: list[Seg] = []
        for s in elf.iter_segments():
            if s["p_type"] != "PT_LOAD":
                continue
            segs.append(
                Seg(
                    vaddr=int(s["p_vaddr"]),
                    memsz=int(s["p_memsz"]),
                    off=int(s["p_offset"]),
                    filesz=int(s["p_filesz"]),
                )
            )
    return blob, segs


def vaddr_read_u8(blob: bytes, segs: list[Seg], addr: int) -> int:
    for seg in segs:
        if seg.file_backed(addr, 1):
            o = seg.vaddr_to_off(addr)
            return blob[o]
        if seg.contains(addr, 1):
            return 0  # bss
    raise KeyError(f"unmapped vaddr 0x{addr:x}")


def vaddr_read_bytes(blob: bytes, segs: list[Seg], addr: int, n: int) -> bytes:
    out = bytearray()
    for i in range(n):
        out.append(vaddr_read_u8(blob, segs, addr + i))
    return bytes(out)


def mem_abs(insn_addr: int, insn_size: int, disp: int) -> int:
    # RIP-relative: next rip + disp
    return insn_addr + insn_size + disp


def canon_reg_name(cs, reg_id: int) -> str:
    # Map any subregister to its GPR group (rax/rbx/.../r15).
    name = cs.reg_name(reg_id)
    # strip size suffixes
    for suf in ("b", "w", "d"):
        if name.endswith(suf) and name not in ("r8b", "r9b", "r10b", "r11b", "r12b", "r13b", "r14b", "r15b"):
            name = name[:-1]
            break
    # al/ah/ax/eax -> rax etc; same for others
    m = {
        "al": "rax",
        "ah": "rax",
        "ax": "rax",
        "eax": "rax",
        "bl": "rbx",
        "bh": "rbx",
        "bx": "rbx",
        "ebx": "rbx",
        "cl": "rcx",
        "ch": "rcx",
        "cx": "rcx",
        "ecx": "rcx",
        "dl": "rdx",
        "dh": "rdx",
        "dx": "rdx",
        "edx": "rdx",
        "sil": "rsi",
        "si": "rsi",
        "esi": "rsi",
        "dil": "rdi",
        "di": "rdi",
        "edi": "rdi",
        "r8b": "r8",
        "r8w": "r8",
        "r8d": "r8",
        "r9b": "r9",
        "r9w": "r9",
        "r9d": "r9",
        "r10b": "r10",
        "r10w": "r10",
        "r10d": "r10",
        "r11b": "r11",
        "r11w": "r11",
        "r11d": "r11",
        "r12b": "r12",
        "r12w": "r12",
        "r12d": "r12",
        "r13b": "r13",
        "r13w": "r13",
        "r13d": "r13",
        "r14b": "r14",
        "r14w": "r14",
        "r14d": "r14",
        "r15b": "r15",
        "r15w": "r15",
        "r15d": "r15",
        "rax": "rax",
        "rbx": "rbx",
        "rcx": "rcx",
        "rdx": "rdx",
        "rsi": "rsi",
        "rdi": "rdi",
        "bpl": "rbp",
        "bp": "rbp",
        "ebp": "rbp",
        "spl": "rsp",
        "sp": "rsp",
        "esp": "rsp",
        "r8": "r8",
        "r9": "r9",
        "r10": "r10",
        "r11": "r11",
        "r12": "r12",
        "r13": "r13",
        "r14": "r14",
        "r15": "r15",
        "rbp": "rbp",
        "rsp": "rsp",
    }
    return m.get(name, name)


class Sym:
    def __init__(self, xbytes: list[z3.BitVecRef]):
        self.x = xbytes
        self.reg: Dict[str, z3.BitVecRef] = {}
        self.stack: Dict[int, z3.BitVecRef] = {}
        self.rsp_delta = 0

    def undef(self, tag: str, pc: int) -> z3.BitVecRef:
        return z3.BitVec(f"undef_{tag}_{pc:x}", 8)

    def get_reg(self, name: str, pc: int) -> z3.BitVecRef:
        if name not in self.reg:
            self.reg[name] = self.undef(name, pc)
        return self.reg[name]

    def set_reg(self, name: str, v: z3.BitVecRef) -> None:
        self.reg[name] = v

    def stack_key(self, disp: int) -> int:
        return self.rsp_delta + disp

    def load_stack(self, disp: int, pc: int) -> z3.BitVecRef:
        k = self.stack_key(disp)
        return self.stack.get(k, self.undef(f"stk_{k}", pc))

    def store_stack(self, disp: int, v: z3.BitVecRef) -> None:
        self.stack[self.stack_key(disp)] = v

    def load_global_lsb(
        self, blob: bytes, segs: list[Seg], abs_addr: int, size: int, pc: int
    ) -> z3.BitVecRef:
        if INPUT_BASE <= abs_addr < INPUT_BASE + INPUT_LEN:
            return self.x[abs_addr - INPUT_BASE]
        # dword/word loads: lsb is still low byte's lsb
        if INPUT_BASE <= abs_addr < INPUT_BASE + INPUT_LEN and size in (2, 4, 8):
            return self.x[abs_addr - INPUT_BASE]
        try:
            b = vaddr_read_u8(blob, segs, abs_addr)
        except KeyError:
            return self.undef(f"mem_{abs_addr:x}", pc)
        return z3.BitVecVal(b & 0xFF, 8)


def solve(path: str) -> str:
    blob, segs = load_segs(path)
    # Fetch bytes from the file-backed portion of the LOAD segment that contains FUNC_START.
    seg = next((s for s in segs if s.file_backed(FUNC_START, 1)), None)
    if seg is None:
        raise RuntimeError(f"FUNC_START 0x{FUNC_START:x} not in file-backed segment")
    max_len = (seg.vaddr + seg.filesz) - FUNC_START
    code = vaddr_read_bytes(blob, segs, FUNC_START, max_len)

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    x = [z3.BitVec(f"b_{i}", 8) for i in range(INPUT_LEN)]
    st = Sym(x)

    def op_byte(insn, op) -> z3.BitVecRef:
        pc = insn.address
        if op.type == X86_OP_REG:
            return st.get_reg(canon_reg_name(md, op.reg), pc)
        if op.type == X86_OP_IMM:
            return z3.BitVecVal(op.imm & 0xFF, 8)
        if op.type == X86_OP_MEM:
            m = op.mem
            if m.base != 0 and md.reg_name(m.base) == "rsp":
                return st.load_stack(m.disp, pc)
            if m.base != 0 and md.reg_name(m.base) == "rip":
                abs_addr = mem_abs(insn.address, insn.size, m.disp)
                return st.load_global_lsb(blob, segs, abs_addr, op.size, pc)
            raise RuntimeError(f"unsupported mem base at 0x{pc:x}: {insn.mnemonic} {insn.op_str}")
        raise RuntimeError(f"unsupported operand type at 0x{pc:x}: {insn.mnemonic} {insn.op_str}")

    def write_op(insn, op, v: z3.BitVecRef) -> None:
        pc = insn.address
        if op.type == X86_OP_REG:
            st.set_reg(canon_reg_name(md, op.reg), v)
            return
        if op.type == X86_OP_MEM:
            m = op.mem
            if m.base != 0 and md.reg_name(m.base) == "rsp":
                st.store_stack(m.disp, v)
                return
            # writes to global/bss are irrelevant for return lsb; ignore.
            if m.base != 0 and md.reg_name(m.base) == "rip":
                return
            raise RuntimeError(f"unsupported mem write at 0x{pc:x}: {insn.mnemonic} {insn.op_str}")
        raise RuntimeError(f"unsupported write operand at 0x{pc:x}: {insn.mnemonic} {insn.op_str}")

    end_pc = None
    for insn in md.disasm(code, FUNC_START):
        pc = insn.address

        mnem = insn.mnemonic
        ops = insn.operands

        if mnem == "ret":
            end_pc = pc
            break

        if mnem == "push":
            st.rsp_delta -= 8
            # store pushed value lsb (rarely used)
            v = op_byte(insn, ops[0])
            st.stack[st.rsp_delta] = v
            continue
        if mnem == "pop":
            v = st.stack.get(st.rsp_delta, st.undef("pop", pc))
            write_op(insn, ops[0], v)
            st.rsp_delta += 8
            continue
        if mnem == "sub" and ops[0].type == X86_OP_REG and md.reg_name(ops[0].reg) == "rsp":
            st.rsp_delta -= int(ops[1].imm)
            continue
        if mnem == "add" and ops[0].type == X86_OP_REG and md.reg_name(ops[0].reg) == "rsp":
            st.rsp_delta += int(ops[1].imm)
            continue

        if mnem in ("mov", "movzx"):
            v = op_byte(insn, ops[1])
            write_op(insn, ops[0], v)
            continue

        if mnem == "not":
            v = op_byte(insn, ops[0]) ^ z3.BitVecVal(0xFF, 8)
            write_op(insn, ops[0], v)
            continue

        if mnem == "and":
            a = op_byte(insn, ops[0])
            b = op_byte(insn, ops[1])
            v = a & b
            write_op(insn, ops[0], v)
            continue

        if mnem == "or":
            a = op_byte(insn, ops[0])
            b = op_byte(insn, ops[1])
            v = a | b
            write_op(insn, ops[0], v)
            continue

        if mnem == "xor":
            a = op_byte(insn, ops[0])
            b = op_byte(insn, ops[1])
            if ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG and ops[0].reg == ops[1].reg:
                v = z3.BitVecVal(0, 8)
            else:
                v = a ^ b
            write_op(insn, ops[0], v)
            continue

        if mnem in ("nop", "endbr64"):
            continue

        # The verifier circuit is straight-line boolean ops; anything else is unexpected.
        raise RuntimeError(f"unexpected insn at 0x{pc:x}: {mnem} {insn.op_str}")

    if end_pc is None:
        raise RuntimeError("did not hit ret; disassembly range too small")

    s = z3.Solver()
    # Main checks (unsigned char)return != 0
    rax = st.get_reg("rax", end_pc)
    s.add(rax != 0)
    # main additionally requires (dword at 0x15350) & 0x10000 != 0, which implies input[754] LSB == 1.
    s.add((x[754] & 1) == 1)
    # Input must be ASCII '0'/'1' (shared upper 7 bits).
    for i in range(INPUT_LEN):
        s.add((x[i] & 0xFE) == 0x30)

    if s.check() != z3.sat:
        raise RuntimeError("UNSAT")
    m = s.model()

    out = []
    for i in range(INPUT_LEN):
        bv = m.eval(x[i], model_completion=True).as_long() & 0xFF
        out.append("1" if (bv & 1) else "0")
    return "".join(out)


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else "./three_sat_problem"
    sol = solve(path)
    print(sol)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

Solved by: yappare

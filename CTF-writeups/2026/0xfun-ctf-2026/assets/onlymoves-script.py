#!/usr/bin/env python3
import os
import re
import subprocess
from dataclasses import dataclass

BIN = os.path.join(os.getcwd(), 'only_moves')
PRELOAD = os.path.join(os.getcwd(), 'hook_oracle.so')

# Bytes scanf("%s") will stop on (plus NUL which can't exist inside the string).
FORBIDDEN = {0x00, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x20}

ORACLE_RE = re.compile(r"\[oracle\]\s+m=([0-9a-f]{8})\s+exp=([0-9a-f]{56})\s+got=([0-9a-f]{56})", re.I)


def bxor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


@dataclass
class OracleResult:
    ok: bool
    exp: bytes | None
    got: bytes | None
    raw: bytes


def run_with_preload(inp: bytes, timeout_s: int = 2) -> OracleResult:
    if len(inp) != 28:
        raise ValueError('need exactly 28 bytes')
    if any(b in FORBIDDEN for b in inp):
        raise ValueError('input contains forbidden byte')

    env = os.environ.copy()
    env['LD_PRELOAD'] = PRELOAD

    p = subprocess.run(
        [BIN],
        input=inp + b"\n",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        timeout=timeout_s,
    )

    out = p.stdout
    if b"Correct!" in out:
        return OracleResult(ok=True, exp=None, got=None, raw=out)

    m = ORACLE_RE.search(out.decode('latin1', errors='ignore'))
    if not m:
        raise RuntimeError('no oracle line found; output was: ' + repr(out[:200]))

    exp = bytes.fromhex(m.group(2))
    got = bytes.fromhex(m.group(3))
    return OracleResult(ok=False, exp=exp, got=got, raw=out)


def build_delta_inverse(ref_inp: bytes, ref_out: bytes, i: int) -> dict[int, int]:
    """Build inv map: delta_value -> input_byte for input position i."""
    start = i ^ 1
    inv: dict[int, int] = {}

    base = bytearray(ref_inp)

    for v in range(1, 256):
        if v in FORBIDDEN:
            continue
        base[i] = v
        r = run_with_preload(bytes(base))
        if r.ok:
            # Shouldn't happen during table building.
            raise RuntimeError('unexpected correct during table build')
        delta = bxor(r.got, ref_out)

        # Expected structure (verified empirically): delta is 0 up to start, then constant suffix.
        dv = delta[start]
        if any(delta[j] != 0 for j in range(start)):
            raise RuntimeError(f'delta prefix non-zero at i={i} v={v:#x} start={start}')
        if any(delta[j] != dv for j in range(start, 28)):
            raise RuntimeError(f'delta suffix not constant at i={i} v={v:#x} start={start}')

        # Invertible mapping expected; detect collisions.
        if dv in inv and inv[dv] != v:
            raise RuntimeError(f'non-invertible delta map at i={i}: dv={dv:#x} v={v:#x} prev={inv[dv]:#x}')
        inv[dv] = v

    return inv


def main():
    ref_byte = 0x61  # 'a'
    if ref_byte in FORBIDDEN:
        raise RuntimeError('bad ref byte')

    ref_inp = bytes([ref_byte]) * 28
    r0 = run_with_preload(ref_inp)
    if r0.ok:
        print('ref input is already correct?')
        return

    target = r0.exp
    ref_out = r0.got

    # Build inverse delta maps per position.
    inv_maps = []
    for i in range(28):
        inv_maps.append(build_delta_inverse(ref_inp, ref_out, i))

    # Solve:
    # y_delta = target XOR ref_out
    # Let acc[j] = XOR of delta_i(x[i]) for all i with (i^1) <= j.
    # With the observed structure, acc[j] == y_delta[j].
    # The unique byte with start=j is i = j^1, and its delta is:
    #   delta_i = acc[j] XOR acc[j-1] == y_delta[j] XOR y_delta[j-1]
    y_delta = bxor(target, ref_out)

    sol = bytearray(28)
    prev = 0
    for j in range(28):
        dv = y_delta[j] ^ prev
        i = j ^ 1
        if dv not in inv_maps[i]:
            raise RuntimeError(f'no inverse for i={i} (start={j}) dv={dv:#x}')
        sol[i] = inv_maps[i][dv]
        prev = y_delta[j]

    # Final sanity check
    r = run_with_preload(bytes(sol))
    if not r.ok:
        raise RuntimeError('computed solution did not validate (still Wrong)')

    # Print as latin1 to preserve any non-ASCII bytes.
    print(bytes(sol).decode('latin1'))


if __name__ == '__main__':
    main()
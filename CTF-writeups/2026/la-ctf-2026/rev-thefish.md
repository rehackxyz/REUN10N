# rev - the-fish

```
#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
FISH = HERE / "fish.py"


def extract_target_int(fish_src: str) -> int:
    m = re.search(r"n\s*==\s*(\d+)\s*:", fish_src)
    if not m:
        raise ValueError("Could not find target integer comparison in fish.py")
    return int(m.group(1))


def invert_encoding(target: int) -> bytes:
    """
    Invert the encoding used by fisherator.

    The output integer is essentially:
      out = 1 || parity_bits || 0   (as a binary string)

    Where parity_bits is the sequence produced while reducing N to 1 using:
      if N even: N = N/2  (emit 0)
      if N odd:  N = 3N+1 (emit 1)

    This function recovers N by reversing the steps from the bits in target.
    """
    b = bin(target)[2:]
    if len(b) < 3 or b[0] != "1" or b[-1] != "0":
        raise ValueError("Target integer does not match expected framing bits")

    mid = b[1:-1]  # strip leading '1' and trailing '0'

    n = 2
    for bit in reversed(mid):
        if bit == "0":
            n *= 2
        elif bit == "1":
            num = 2 * n - 1
            if num % 3 != 0:
                raise ValueError("Non-invertible step encountered (num % 3 != 0)")
            n = num // 3
        else:
            raise ValueError("Unexpected non-bit character in binary string")

    nbytes = (n.bit_length() + 7) // 8
    return n.to_bytes(nbytes, "big")


def main(argv: list[str]) -> int:
    verify = "--verify" in argv

    fish_src = FISH.read_text(encoding="utf-8", errors="strict")
    target = extract_target_int(fish_src)
    raw = invert_encoding(target)

    try:
        flag = raw.decode("utf-8")
    except UnicodeDecodeError:
        flag = raw.decode("latin-1")

    sys.stdout.write(flag + "\n")

    if verify:
        # Run fish.py non-interactively with the recovered flag on stdin.
        p = subprocess.run(
            [sys.executable, str(FISH)],
            input=(flag + "\n").encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        sys.stdout.write(p.stdout.decode("utf-8", errors="replace"))
        return p.returncode

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

```
$ python fish.py
><> ><>. (Enter the flag): lactf{7h3r3_m4y_83_50m3_155u35_w17h_7h15_1f_7h3_c011472_c0nj3c7ur3_15_d15pr0v3n}
><>? ><>! (Indeed, that is the flag!)
```

Solved by Zeqzoq

Solved by: yappare
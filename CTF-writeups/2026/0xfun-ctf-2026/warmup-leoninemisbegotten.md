# warmup - Leonine Misbegotten

```python
import base64, hashlib
from pathlib import Path

ROUNDS = 16
data = Path("output").read_bytes()

def sha1d(x: bytes) -> bytes:
    return hashlib.sha1(x).digest()

def try_decode(name: str, b: bytes):
    try:
        if name == "b16":
            return base64.b16decode(b, casefold=True)
        if name == "b32":
            return base64.b32decode(b, casefold=True)
        if name == "b64":
            pad = (-len(b)) % 4
            return base64.b64decode(b + b"=" * pad, validate=False)
        if name == "b85":
            return base64.b85decode(b)
    except Exception:
        return None

schemes = ["b16", "b32", "b64", "b85"]
path = []

for _ in range(ROUNDS):
    enc, chk = data[:-20], data[-20:]
    found = None
    for s in schemes:
        dec = try_decode(s, enc)
        if dec is not None and sha1d(dec) == chk:
            found = (s, dec)
            break
    if not found:
        raise RuntimeError("No valid scheme found (corrupt data?)")
    s, data = found
    path.append(s)

print("reverse schemes:", path)
print("flag:", data.decode())
```

FLAG:`0xfun{p33l1ng_l4y3rs_l1k3_an_0n10n}`

Solved by Zeqzoq

Solved by: ha1qal
# rev - Chip8 Emulator

```python
#!/usr/bin/env python3
import base64, re, subprocess
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

BIN = "./chip8Emulator"

KEY = b"tLeBHJvLCDHDEACHCBE8HCSAIFidAGGI"

def get_b64_blob():
    out = subprocess.check_output(["strings", "-n", "20", BIN], text=True, errors="ignore").splitlines()
    # pick the long base64-looking line
    for line in out:
        line=line.strip()
        if re.fullmatch(r"[A-Za-z0-9+/]{300,}={0,2}", line):
            return line
    raise RuntimeError("base64 blob not found")

def b64decode_fix(s: str) -> bytes:
    s = s.strip()
    s += "=" * ((4 - len(s) % 4) % 4)
    return base64.b64decode(s)

def looks_like_b64_text(b: bytes) -> bool:
    try:
        s = b.decode().strip()
    except:
        return False
    if not re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
        return False
    return (len(s) % 4) == 0

data = get_b64_blob().encode()

# Peel alternating: base64 -> (IV||CT) -> AES-CBC -> base64 -> ...
for _ in range(20):
    if looks_like_b64_text(data):
        data = b64decode_fix(data.decode())
        continue

    if len(data) >= 32 and len(data) % 16 == 0:
        iv, ct = data[:16], data[16:]
        pt = AES.new(KEY, AES.MODE_CBC, iv).decrypt(ct)
        data = unpad(pt, 16)
        continue

    break

print(data.decode())
```
FLAG:`0xfunCTF2025{N0w_y0u_h4v3_clear_1dea_H0w_3mulators_WoRK}`

Solved by: ha1qal
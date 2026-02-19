# crypto - Hawk_II

```python
#!/usr/bin/env python3
import re, hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def main():
    data = open("output.txt", "r", encoding="utf-8").read()

    iv_hex  = re.search(r'iv\s*=\s*"([0-9a-fA-F]+)"', data).group(1)
    enc_hex = re.search(r'enc\s*=\s*"([0-9a-fA-F]+)"', data).group(1)

    # Grab EXACT tuple string that was printed for sk (this matches str(sk))
    m = re.search(r'sk\s*=\s*(\(.+?\))\s*leak_data\s*=', data, flags=re.S)
    if not m:
        raise SystemExit("Failed to extract sk tuple string")
    sk_str = m.group(1)

    key = hashlib.sha256(sk_str.encode()).digest()
    iv  = bytes.fromhex(iv_hex)
    ct  = bytes.fromhex(enc_hex)

    pt = unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(ct), 16)
    print(pt.decode(errors="replace"))

if __name__ == "__main__":
    main()
```
FLAG:`0xfun{tOO_LLL_256_B_kkkkKZ_t4e_f14g_F14g}`

Solved by: ha1qal
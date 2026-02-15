# re - E4sy P3asy

```
#!/usr/bin/env python3
import hashlib
import string

# Fixed salt from the binary
salt = "KnightCTF_2026_s@lt"

# off_3CA0 hashes (23 entries, in order)
hashes = [
    "781011edfb2127ee5ff82b06bb1d2959",
    "4cf891e0ddadbcaae8e8c2dc8bb15ea0",
    "d06d0cbe140d0a1de7410b0b888f22b4",
    "d44c9a9b9f9d1c28d0904d6a2ee3e109",
    "e20ab37bee9d2a1f9ca3d914b0e98f09",
    "d0beea4ce1c12190db64d10a82b96ef8",
    "ac87da74d381d253820bcf4e5f19fcea",
    "ce3f3a34a04ba5e5142f5db272b6cb1f",
    "13843aca227ef709694bbfe4e5a32203",
    "ca19a4c4eb435cb44d74c1e589e51a10",
    "19edec8e46bdf97e3018569c0a60baa3",
    "972e078458ce3cb6e32f795ff4972718",
    "071824f6039981e9c57725453e005beb",
    "66cd6098426b0e69e30e7fa360310728",
    "f78d152df5d277d0ab7d25fb7d1841f3",
    "dba3a36431c4aaf593566f7421abaa22",
    "8820bbdad85ebee06632c379231cfb6b",
    "722bc7cde7d548b81c5996519e1b0f0f",
    "c2862c390c830eb3c740ade576d64773",
    "94da978fe383b341f9588f9bab246774",
    "bea3bb724dbd1704cf45aea8e73c01e1",
    "ade2289739760fa27fd4f7d4ffbc722d",
    "3cd0538114fe416b32cdd814e2ee57b3",
]

# Full printable ASCII (binary allows ANY %c)
charset = ''.join(chr(i) for i in range(32, 127))

flag_inner = ""

for i, target in enumerate(hashes):
    found = False
    for c in charset:
        payload = f"{salt}{i}{c}".encode()
        if hashlib.md5(payload).hexdigest() == target:
            print(f"[+] Found char {i}: {repr(c)}")
            flag_inner += c
            found = True
            break

    if not found:
        raise RuntimeError(f"[-] No match found at index {i}")

print("\nFINAL FLAG:")
print(f"KCTF{{{flag_inner}}}")
```

Flag: `KCTF{_L0TS_oF_bRuTE_foRCE_:P} `
SOLVED by Ha1qal

Solved by: yappare
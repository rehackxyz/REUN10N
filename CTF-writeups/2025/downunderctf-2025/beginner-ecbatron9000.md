## Solution:
ECB leaks bytes because it encrypts every 16-byte block alone
you pad so the unknown byte is at the block’s end:
```
[pad = 15 bytes][secret so far][?]
```
then for each guess `g`
```
encrypt [pad][secret][g] > get 1st, 2nd cipher blocks  
take the same block index  
map block > g
```
lastly:
```
if oracle_block == one of map’s blocks  
    that g is the secret byte
```
rinse n repeat
```py
import base64


import requests
import string,  sys

base_url   = "https://beginner-ecb-a-tron-9000-1fc633e2ebf6.2025.ductf.net"
block_size=16
secret = b""

for _ in range(64):

    pad_len =  block_size-1 - len(secret) % block_size
    prefix= b"A"*pad_len

    data=base64.b64encode(prefix).decode()
    response  = requests.post(f"{base_url}/encrypt",json={"data":data})
    ciphertext = base64.b64decode(response.json()["ciphertext"])



    idx = len(secret)//block_size
    target_block = ciphertext[idx*block_size:(idx+1)*block_size]

    candidates = [prefix+secret+ch.encode() for ch in string.printable]

    batch = [base64.b64encode(c).decode() for c in candidates]
    batch_resp= requests.post(f"{base_url}/encrypt_batch", json={"data":batch})
    cipher_texts = batch_resp.json()["ciphertexts"]

    mapping={ base64.b64decode(c)[idx*block_size:(idx+1)*block_size]: p[-1:]
              for p,c in zip(candidates, cipher_texts) }

    if target_block in mapping:
        byte = mapping[target_block]

        secret += byte
        sys.stdout.write(byte.decode())
        sys.stdout.flush()
        if byte==b"}": break


print("\nSecret:", secret.decode())
```

Flag:  `DUCTF{DONTUSEECBPLEASE}`

Solved by: vicevirus
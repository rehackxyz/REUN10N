# idk cipher

Solved by: @hikki

- Category: crypto
- Description: I spent a couple of hours with ???; now I am the world's best cryptographer!!! note: the flag contents will just random chars-- not english/leetspeak

Cipher Text: QRVWUFdWEUpdXEVGCF8DVEoYEEIBBlEAE0dQAURFD1I=

Please wrap the flag with pctf{}.

- Challenge File: encode.py

### Solution:

```py
import base64

def decode(b64_encoded, key):

    encoded = base64.b64decode(b64_encoded).decode()

    output = []
    halflen = len(encoded) // 2


    decoded = []
    for i in range(halflen):
        enc_p1 = encoded[2 * i]
        enc_p2 = encoded[2 * i + 1]

        c1 = chr(ord(enc_p1) ^ ord(key[i % len(key)]))
        c2 = chr(ord(enc_p2) ^ ord(key[i % len(key)]))

        decoded.append(c1)
        decoded.insert(0, c2)
    
    usr_input = ''.join(decoded)

    usr_input = usr_input[halflen:] + usr_input[:halflen]
    return usr_input


key = "secretkey"
b64_encoded = "QRVWUFdWEUpdXEVGCF8DVEoYEEIBBlEAE0dQAURFD1I=" 

decoded = decode(b64_encoded, key)
print("Decoded user input:", decoded)
```

**Flag:** `pctf{234c81cf3cd2a50d91d5cc1a1429855f}`


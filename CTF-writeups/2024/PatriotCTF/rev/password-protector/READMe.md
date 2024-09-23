# Password Protector

Solved by: @Cookies to SELL

- Category: reverse
- Description: 

We've been after a notorious skiddie who took the "Is it possible to have a completely secure computer system" question a little too literally. After he found out we were looking for them, they moved to live at the bottom of the ocean in a concrete box to hide from the law. Eventually, they'll have to come up for air...or get sick of living in their little watergapped world. They sent us this message and executable. Please get their password so we can be ready.

"Mwahahaha you will nOcmu{9gtufever crack into my passMmQg8G0eCXWi3MY9QfZ0NjCrXhzJEj50fumttU0ympword, i'll even give you the key and the executable:::: Zfo5ibyl6t7WYtr2voUEZ0nSAJeWMcN3Qe3/+MLXoKL/p59K3jgV"

- Challenge File: passwordProtector.pyc

### Step 1: Figure out python module version 

```
$ file passwordProtector.pyc
passwordProtector.pyc: Byte-compiled Python module for CPython 3.11, timestamp-based, .py timestamp: Mon Jun 24 01:36:28 2024 UTC, .py size: 854 bytes
```

### Step 2: Use pylingual.io to decompile
- Both uncompyle6 and pycdc won't work due to the file is compile with CPython
- Use [pylingual.io](https://pylingual.io/)

After decompilation:

```py
import os
import secrets
from base64 import *

def promptGen():
    flipFlops = lambda x: chr(ord(x) + 1)
    with open('topsneaky.txt', 'rb') as f:
        first = f.read()
    bittys = secrets.token_bytes(len(first))
    onePointFive = int.from_bytes(first) ^ int.from_bytes(bittys)
    second = onePointFive.to_bytes(len(first))
    third = b64encode(second).decode('utf-8')
    bittysEnc = b64encode(bittys).decode('utf-8')
    fourth = ''
    for each in third:
        fourth += flipFlops(each)
    fifth = f"Mwahahaha you will n{fourth[0:10]}ever crack into my pass{fourth[10:]}word, i'll even give you the key and the executable:::: {bittysEnc}"
    return fifth

def main():
    print(promptGen())
if __name__ == '__main__':
    main()
```

From the decompile code, it uses xor and base64 encoding to generate a message and based on the challenge descripton, it has the message `Mwahahaha you will nOcmu{9gtufever crack into my passMmQg8G0eCXWi3MY9QfZ0NjCrXhzJEj50fumttU0ympword, i'll even give you the key and the executable:::: Zfo5ibyl6t7WYtr2voUEZ0nSAJeWMcN3Qe3/+MLXoKL/p59K3jgV`

To decrypt the message, reverse the promptGen() function

### Step 3: Reverse promptGen() function

```py
import secrets
from base64 import b64decode

fourth = "Ocmu{9gtufMmQg8G0eCXWi3MY9QfZ0NjCrXhzJEj50fumttU0ymp"
bittysEnc = "Zfo5ibyl6t7WYtr2voUEZ0nSAJeWMcN3Qe3/+MLXoKL/p59K3jgV"

def reverse_flipFlops(x):
    return chr(ord(x) - 1)

third_reversed = ''.join(reverse_flipFlops(each) for each in fourth)

try:
    second = b64decode(third_reversed)
except Exception as e:
    print(f"Decoding error: {e}")


try:
    bittys = b64decode(bittysEnc)
except Exception as e:
    print(f"Decoding error: {e}")

length_of_second = len(second)
first_reconstructed = int.from_bytes(second) ^ int.from_bytes(bittys)

original_bytes = first_reconstructed.to_bytes(length_of_second, 'big')

print(original_bytes)
```

Here we reverse by shifting the characters back with `chr(ord(x)-1)`, and decode with base64 for `third_reversed` and `bittysEnc`. After xor both and the result is converted to bytes. 

**Flag:** `PCTF{I_<3_$3CUR1TY_THR0UGH_0B5CUR1TY!!}`

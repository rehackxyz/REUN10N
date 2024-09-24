# Making Baking Pancakes

Solved by: @hikki

- Category: misc
- Description: How many layers are on your pancakes?

### Solution:

```py
import base64
from pwn import *

conn = remote("chal.pctf.competitivecyber.club", 9001)


def decode_challenge(challenge):
    decoded_challenge = base64.b64decode(challenge).decode("utf-8")
    n = int(decoded_challenge.split("|")[1])
    for _ in range(n):
        decoded_challenge = base64.b64decode(decoded_challenge.split("|")[0]).decode("utf-8")
    return decoded_challenge.split("|")[0]

for challenge_iteration in range(1000):
    conn.recvuntil(b"Challenge: ")
    challenge = conn.recvline().decode("utf-8")
    # print(f"Received challenge {challenge_iteration}: {challenge}")

    decoded_challenge = decode_challenge(challenge)
    # print(f"Decoded challenge: {decoded_challenge}")

    conn.sendline(f"{decoded_challenge}|{challenge_iteration}")
    print(f"Sent response {challenge_iteration}: {decoded_challenge}|{challenge_iteration}")


print(conn.recvline().decode("utf-8"))
print(conn.recvline().decode("utf-8"))
print(conn.recvline().decode("utf-8"))
```

**flag:** `pctf{store_bought_pancake_batter_fa82370}`

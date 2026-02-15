# rev - AuraTester2000

SOLVED by Ha1qal

```
from pwn import *
import re

# Server details
HOST = 'auratester.ctf.pascalctf.it'
PORT = 7001

# Flattened list to handle the space in "filippo boschi"
word_bank = ["tungtung", "trallalero", "filippo", "boschi", "zaza", "lakaka", "gubbio", "cucinato"]

def solve_aura(encoded_str):
    chunks = encoded_str.split(" ")
    decoded_list = []

    for chunk in chunks:
        # Get just the letters to help with matching
        letters = "".join(re.findall(r'[a-zA-Z]', chunk))
        
        for word in word_bank:
            # Match by checking if the start character (ASCII or char) aligns
            # and if the word length/structure makes sense
            if chunk.startswith(str(ord(word[0]))) or chunk.startswith(word[0]):
                # If we have letters, ensure they exist in the target word
                if not letters or all(c in word for c in letters):
                    decoded_list.append(word)
                    break
    
    return " ".join(decoded_list)

# --- Connection ---
io = remote(HOST, PORT)
io.sendlineafter(b"> ", b"AuraGod")

# Farm 700 Aura
io.sendlineafter(b"> ", b"1")
for ans in [b"yes", b"no", b"yes", b"no"]:
    io.sendlineafter(b"> ", ans)

# Start Test
io.sendlineafter(b"> ", b"3")
io.recvuntil(b"secret phrase: ")
challenge = io.recvline().decode().strip()
log.info(f"Challenge: {challenge}")

solution = solve_aura(challenge)
log.success(f"Sending: {solution}")

io.sendlineafter(b"> ", solution.encode())
print(io.recvall().decode())
```

Flag:`⁨pascalCTF{Y0u_4r3_th3_r34l_4ur4_f1n4l_b0s5}⁩`

Solved by: yappare
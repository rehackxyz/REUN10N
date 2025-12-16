XOR_KEY = [0x42, 0x73, 0x21, 0x69, 0x37]
MAGIC_ADD = 0x2A
FLAG_LEN = 30

## Chatgpt solve it
buffer = TARGET.copy()

print("Starting decryption...")

# Reverse OPERATION 4: XOR each byte with its position
print("[1/4] Reversing coordinate calibration...")
for i in range(FLAG_LEN):
    buffer[i] ^= i

# Reverse OPERATION 3: Subtract magic constant
print("[2/4] Reversing gravitational shift...")
for i in range(FLAG_LEN):
    buffer[i] = (buffer[i] - MAGIC_ADD) & 0xFF

# Reverse OPERATION 2: Swap adjacent byte pairs again
print("[3/4] Reversing spatial transposition...")
for i in range(0, FLAG_LEN, 2):
    temp = buffer[i]
    buffer[i] = buffer[i + 1]
    buffer[i + 1] = temp

# Reverse OPERATION 1: XOR with rotating key again
print("[4/4] Reversing quantum entanglement cipher...")
for i in range(FLAG_LEN):
    buffer[i] ^= XOR_KEY[i % 5]

print("Decrypted flag: ", end="")
for i in range(FLAG_LEN):
    print(chr(buffer[i]), end="")
print()
```

Flag: PCTF{0x_M4rks_tH3_sp0t_M4t3ys}

Solved by: amkim13
# Solution
```
# Bytes from px 100 output (first 100 bytes of intro function at 0x4017E1)
intro_bytes = bytes.fromhex(
    "55 89 e5 81 ec 58 01 00 00 8d 85 b8 fe ff ff 89 " +
    "44 24 08 8d 85 1c ff ff ff 89 44 24 04 8d 45 80 " +
    "89 04 24 e8 57 fc ff ff c7 05 20 90 40 00 aa 55 " +
    "aa 55 c7 45 f4 00 00 00 00 eb 29 8d 55 80 8b 45 " +
    "f4 01 d0 0f b6 00 0f be c0 89 04 24 e8 56 2d 00 " +
    "00 c7 04 24 28 00 00 00 e8 4a 2e 00 00 83 ec 04 " +
    "83 45 f4 01 8d 45 80 89 04 24 e8 00 2d 00 00"
)

# Make sure we have exactly 100 bytes
if len(intro_bytes) < 100:
    # Pad with zeros if needed
    intro_bytes = intro_bytes + b'\x00' * (100 - len(intro_bytes))
else:
    intro_bytes = intro_bytes[:100]

print(f"Intro bytes (first 20): {intro_bytes[:20].hex()}")
print(f"Total bytes: {len(intro_bytes)}")

# Compute jointStep transformation
jointStep = 0x55AA55AA  # Initial value

for i in range(100):
    # Transformation: jointStep = code_byte ^ ((jointStep << 5) ^ (jointStep >> 3))
    code_byte = intro_bytes[i]
    
    # Note: We need to simulate 32-bit overflow
    jointStep = jointStep & 0xFFFFFFFF
    
    # Compute (jointStep << 5) ^ (jointStep >> 3)
    shifted = ((jointStep << 5) ^ (jointStep >> 3)) & 0xFFFFFFFF
    
    # XOR with code byte and update
    jointStep = (code_byte ^ shifted) & 0xFFFFFFFF
    
    # Debug: print first few iterations
    if i < 5:
        print(f"Iteration {i}: byte=0x{code_byte:02X}, jointStep=0x{jointStep:08X}")

print(f"\nFinal jointStep value: 0x{jointStep:08X} ({jointStep})")

# Now let's decrypt the flag
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import struct

# Read encrypted data
with open("flag.enc", 'rb') as f:
    encrypted_data = f.read()

print(f"\nEncrypted data length: {len(encrypted_data)} bytes")

# Source strings
s1 = "hehe, aren't we all chasing the light mate?"
s2 = " Lookin' everywhere to find it,"
s3 = " everywhere but within."

# Tokenize function
def tokenize(s, delimiters=" ,.?!'"):
    result = []
    current = ""
    for c in s:
        if c in delimiters:
            if current:
                result.append(current)
                current = ""
        else:
            current += c
    if current:
        result.append(current)
    return result

# Build Str as per the code
Str = ""
Str += tokenize(s1)[0]   # "hehe"
Str += tokenize(s1)[5]   # "chasing"
Str += tokenize(s1)[7]   # "light"
Str += tokenize(s2)[1]   # "everywhere"
Str += tokenize(s2)[3]   # "find"
Str += tokenize(s3)[2]   # "within"

print(f"Str: {Str}")

# Known sassyIV from binary
sassyIV = bytes([0x16, 0x00, 0x05, 0x18, 0x00, 0x15, 0x00, 0x0D, 
                 0x0A, 0x08, 0x0F, 0x00, 0x03, 0x04, 0x04, 0x15])

destination = s1 + s2 + s3
dest_len = len(destination)

# Calculate IV: sassyIV[i] ^ dest_len
iv = bytearray(16)
for i in range(16):
    iv[i] = sassyIV[i] ^ (dest_len & 0xFF)
iv = bytes(iv)

print(f"Destination length: {dest_len}")
print(f"IV: {iv.hex()}")

# Convert jointStep to bytes (little-endian)
jointStep_bytes = struct.pack('<I', jointStep)
print(f"jointStep bytes: {jointStep_bytes.hex()}")

# XOR Str with jointStep bytes
Str_bytes = bytearray(Str.encode())
for j in range(len(Str_bytes)):
    Str_bytes[j] ^= jointStep_bytes[j & 3]
Str_xor = bytes(Str_bytes)

print(f"Str after XOR: {Str_xor.hex()[:50]}...")

# Generate key (SHA-256)
key = hashlib.sha256(Str_xor).digest()
print(f"AES key: {key.hex()[:50]}...")

# Try decryption
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted = cipher.decrypt(encrypted_data)

print(f"\nDecrypted (first 100 bytes): {decrypted[:100]}")

# Try to find flag
for marker in [b'flag{', b'FLAG{', b'ctf{', b'CTF{', b'HTB{']:
    if marker in decrypted:
        idx = decrypted.find(marker)
        end = decrypted.find(b'}', idx)
        if end != -1:
            flag = decrypted[idx:end+1]
            print(f"\n🎉 FLAG FOUND: {flag.decode()}")
            break
else:
    # Try unpadding
    try:
        unpadded = unpad(decrypted, AES.block_size)
        print(f"\nUnpadded data: {unpadded[:200]}")
        # Try to decode as string
        try:
            text = unpadded.decode('utf-8', errors='ignore')
            print(f"As text: {text}")
        except:
            pass
    except:
        print("\nCould not unpad or find flag pattern")
        print("Raw decrypted hex (first 200 bytes):")
        print(decrypted[:200].hex())
```
Flag:nullctf{7H1S_1S_A_N1C3_PL4C3_M8}

Solved by: ha1qal

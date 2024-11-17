# Schrödinger's Pad

Solved by: @Zeqzoq

## Question:
Everyone knows you can't reuse a OTP, but throw in a cat and a box.. Maybe it's secure?

## Solution:
```
def reverse_cat_state_transformation(ciphertext):
    # Reverse the "cat state=alive" transformation: XOR with 0xAC and right shift by 1
    return bytes([((c ^ 0xAC) >> 1) | ((c ^ 0xAC) << 7 & 0xFF) for c in ciphertext])

def hex_to_bytes(hex_str):
    return bytes.fromhex(hex_str)

# Provided data
encrypted_flag_hex = "1b122b1435342d3a5f53164023761b0d2d70275b6d1856491c0257071420170e181b097e611139213e021a0e350e3531455311295f363d4303754e7a4f66035a131c501b7a635e0c110574072d53252634531a4e3a186f2c154d321f06040b42502d1e4b120e3b6452071a2674281c5306690a0314575d6d7c3c4d4711410f433c1b245b0c5e1c0c1c6f470a0461565203344239433929022706760023063618"
ciphertext_hex = "becca8e29a8ea6865e42e6e08e82def69c8eb244b4dcc25efce85cc8ecb440f6ccc4f48aac9ec0c4c0a4bea0eca0b284c2e0c4c2f0a6eac0f0a65ebc4aa2f848c0de44c482a842f4e8ec86c8aac8a8b09a4046f2c8f8b0a4ecf488c8f0caf2f2ceaaf6f8daf0bea646e2f2a886badc42febcdcc8ec5ceab4448af446e64cfa4cb6c6804ade40c8ea4eb048eaecac4c48f28ce4bae880b6c6aac682e6b6fe8842"

# Convert hex strings to byte arrays
encrypted_flag = hex_to_bytes(encrypted_flag_hex)
ciphertext = hex_to_bytes(ciphertext_hex)

# The plaintext we sent ("A" * 160) in bytes
plaintext = b"A" * 160

# Reverse the "cat state=alive" transformation on the received ciphertext
reversed_ciphertext = reverse_cat_state_transformation(ciphertext)

# Derive the key using XOR between the known plaintext and the transformed ciphertext
key = bytes([c ^ 0x41 for c in reversed_ciphertext])

# Decrypt the flag using the derived key
decrypted_flag = bytes([ef ^ k for ef, k in zip(encrypted_flag, key)])
print(decrypted_flag.decode(errors='ignore'))
```

**Flag:** `INTIGRITI{d34d_0r_4l1v3}`

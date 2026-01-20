# Reverse - ReM3

```python
def sub_14C0_decrypt(encrypted_bytes):
    encrypted = bytearray(encrypted_bytes)
    decrypted = bytearray(29)
    
    v2 = 0
    v3 = 0
    v4 = -61  # 0xFFFFFFC3
    
    const1 = 0x2F910ED35CA71942
    const2 = 0x6A124DE908B17733
    
    # We need to process in reverse or track state
    # Actually, we can process forward if we reconstruct
    
    # First, let's compute all the deterministic values
    v6_vals = []
    v7_vals = []
    rot_amounts = []
    v4_vals = [v4]
    
    for i in range(29):
        v6 = v3 + ((const1 >> (8 * (i & 7))) & 0xFF)
        v6_vals.append(v6 & 0xFF)
        v3 += 29
        
        rot_amount = (const2 >> ((8 * i + 16) & 0x38)) & 0xFF
        rot_amounts.append(rot_amount & 7)
        
        v7 = v2 ^ ((const2 >> (8 * (i & 7))) & 0xFF)
        v7_vals.append(v7 & 0xFF)
        v2 += 17
        
        # We can't compute v4 yet without knowing output
        v4_vals.append(None)  # placeholder
    
    # Now decrypt
    v4 = -61
    for i in range(29):
        # Reverse step 8: encrypted[i] = ror8(v8, v4 & 7)
        v8_byte = rol8(encrypted[i], v4 & 7)
        
        # Reverse step 6: v8 = v7 ^ (v4 + v6_byte)
        # So: v4 + v6_byte = v7 ^ v8
        # v6_byte = (v7 ^ v8) - v4
        v6_byte = (v7_vals[i] ^ v8_byte) - v4
        v6_byte &= 0xFF  # Keep as byte
        
        # Reverse step 4: v6_byte = rol8(temp, rot_amount)
        # So: temp = ror8(v6_byte, rot_amount)
        temp = ror8(v6_byte, rot_amounts[i])
        
        # Reverse step 2: temp = data[i] ^ v6_val
        # So: data[i] = temp ^ v6_val
        decrypted[i] = temp ^ v6_vals[i]
        
        # Update v4 for next iteration (same as encryption)
        v4 += encrypted[i] + (((const1 >> ((8 * i + 24) & 0x38)) & 0xFF) ^ 0xA5)
        v4 &= 0xFFFFFFFF  # Keep as 32-bit
    
    return bytes(decrypted)

# Test decryption
if len(target) == 29:
    decrypted = sub_14C0_decrypt(target)
    print(f"Decrypted flag: {decrypted}")
    print(f"Decrypted hex: {decrypted.hex()}")
    
    # Check if it looks like a flag
    if decrypted.startswith(b"KCTF{") and decrypted.endswith(b"}"):
        print("Found flag:", decrypted.decode())
    else:
        print("Doesn't look like a flag... checking encryption")
        # Encrypt back to verify
        reencrypted = sub_14C0_encrypt(decrypted)
        print(f"Re-encrypted: {reencrypted.hex()}")
        print(f"Target:       {target.hex()}")
        print(f"Match: {reencrypted == target}")
```
`KCTF{w3Lc0m3_T0_tHE_r3_w0rLD}`

Solved by: ha1qal
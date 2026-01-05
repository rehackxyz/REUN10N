# Solution
```python
from pwn import *
from Crypto.Util.strxor import strxor

# Configuration
HOST = 'public.ctf.r0devnull.team'
PORT = 3017

def connect():
    # context.log_level = 'debug'  # Uncomment if you need to see exactly what's happening
    return remote(HOST, PORT)

def get_flag_enc(r):
    # Wait for the menu to finish printing before sending input
    r.sendlineafter(b'[3] Get Flag', b'3')
    r.recvuntil(b'flag = ')
    return bytes.fromhex(r.recvline().strip().decode())

def encrypt(r, plaintext):
    r.sendlineafter(b'[3] Get Flag', b'1')
    r.sendlineafter(b'(hex): ', plaintext.hex().encode())
    return bytes.fromhex(r.recvline().strip().decode())

def decrypt(r, ciphertext):
    r.sendlineafter(b'[3] Get Flag', b'2')
    r.sendlineafter(b'(hex): ', ciphertext.hex().encode())
    response = r.recvline().strip().decode()
    if "Nope" in response or "error" in response:
        return None
    return bytes.fromhex(response)

def solve():
    r = connect()
    
    print("[*] Retrieving encrypted flag...")
    # 1. Get the encrypted flag
    flag_enc_full = get_flag_enc(r)
    flag_blocks = [flag_enc_full[i:i+16] for i in range(0, len(flag_enc_full), 16)]
    print(f"[+] Encrypted Flag retrieved ({len(flag_blocks)} blocks)")

    # 2. Recover IV and D_k(0)
    print("[*] Leaking internal state (IV and D_k(0))...")
    # Encrypt 32 bytes of zeros to get two blocks
    zeros_32 = b'\x00' * 32
    ct_zeros = encrypt(r, zeros_32)
    
    c0 = ct_zeros[0:16]
    c1 = ct_zeros[16:32]
    
    # In the encryption scheme: C1 = D_k(0) ^ P0 (where P0 is 0) -> C1 = D_k(0)
    Y = c1 
    # C0 = D_k(0) ^ IV -> IV = C0 ^ D_k(0)
    IV = strxor(c0, Y)
    
    print(f"[+] Recovered IV: {IV.hex()}")
    print(f"[+] Recovered Y (D_k(0)): {Y.hex()}")

    # 3. Decrypt the flag block by block
    recovered_pt = b""
    prev_m = IV # For the first block, the "previous plaintext" is the IV
    
    print("[*] Starting Chosen Ciphertext Attack...")
    
    for i, f_block in enumerate(flag_blocks):
        # We want to force the server to decrypt: M_i = E_k(F_i ^ M_{i-1})
        # We construct a payload: [ Reset Block ] [ Target Block ]
        # Reset Block (A): Y ^ IV. This decrypts to 0 (P_A = 0).
        # Target Block (B): F_i ^ M_{i-1}.
        # Result P_B = E_k(B ^ P_A) = E_k(B ^ 0) = E_k(Target Block).
        
        target_input = strxor(f_block, prev_m)
        
        block_a = strxor(Y, IV)
        block_b = target_input
        
        payload = block_a + block_b
        
        # Send to decryption oracle
        decrypted = decrypt(r, payload)
        
        if decrypted:
            # The result is P_A || P_B. We want P_B (the second 16 bytes).
            m_block = decrypted[16:32]
            recovered_pt += m_block
            prev_m = m_block # Update M_{i-1} for the next iteration
            print(f"    [-] Block {i} recovered: {m_block.hex()} | {m_block}")
        else:
            print(f"    [!] Failed to decrypt block {i}. Server rejected the payload.")
            break
            
    print(f"\n[+] Flag: {recovered_pt.decode(errors='ignore')}")
    r.close()

if __name__ == '__main__':
    solve()
```
Flag:nullctf{z1g_z4g_cr7pt0_fl1p_fl0p}

Solved by: ha1qal

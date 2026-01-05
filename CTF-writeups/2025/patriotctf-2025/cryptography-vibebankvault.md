```
from pwn import *
import bcrypt
import base64
import string
import re

# --- Configuration ---
HOST = '18.212.136.134'
PORT = 6666
_STATIC_SALT = b"$2b$12$C8YQMlqDyz3vGN9VOGBeGu"

def local_vibe_hash(data_bytes):
    """Replicates the server's hash logic for local checking."""
    # Simulating the server logic: 
    # portion = payload[: len(payload) % 256]
    # bcrypt.hashpw(portion, salt)
    
    limit = len(data_bytes) % 256
    portion = data_bytes[:limit]
    
    # Bcrypt itself truncates to 72 bytes, which is the key to Level 1
    digest = bcrypt.hashpw(portion, _STATIC_SALT)
    return f"vb$1${base64.b64encode(digest).decode()}"

def solve():
    r = remote(HOST, PORT)

    # --- LEVEL 1 ---
    r.recvuntil(b"Leaked Note: ")
    leak = r.recvline().strip().decode()
    r.recvuntil(b"Target Hash: ")
    target_hash = r.recvline().strip().decode()
    
    log.info(f"Level 1: Leak size {len(leak)}. Brute forcing last 2 bytes...")
    
    charset = string.ascii_letters + string.digits
    found_pw = None
    
    # We need to find 2 chars such that bcrypt(leak + c1 + c2) matches target
    # Total length will be 72. 72 % 256 = 72. Hash processes all 72 bytes.
    for c1 in charset:
        for c2 in charset:
            candidate = leak + c1 + c2
            # We pass bytes to our local helper
            if local_vibe_hash(candidate.encode()) == target_hash:
                found_pw = candidate
                break
        if found_pw: break
        
    if found_pw:
        log.success(f"Found Level 1 Password: {found_pw}")
        r.sendlineafter(b"Enter password: ", found_pw.encode())
    else:
        log.error("Failed to crack Level 1")
        return

    # --- LEVEL 2 ---
    r.recvuntil(b"prefix: '")
    prefix = r.recvuntil(b"'", drop=True).decode()
    log.info(f"Level 2: Prefix is {prefix}")
    
    # Strategy: Modulo 256 = 0 results in empty hash.
    # String 1: Prefix + padding to 256 bytes
    # String 2: Prefix + padding to 512 bytes
    pad1 = "A" * (256 - len(prefix))
    pad2 = "B" * (512 - len(prefix)) # Use different char to ensure strings are diff
    
    payload = f"{prefix}{pad1},{prefix}{pad2}"
    r.sendlineafter(b"Format: string1,string2", payload.encode())

    # --- LEVEL 3 ---
    r.recvuntil(b"very long (")
    target_len = int(r.recvuntil(b" ", drop=True).decode())
    log.info(f"Level 3: Target length {target_len}")
    
    # Strategy: Send 'B' * (target_len % 256)
    # The hash only sees the modulo length.
    needed_len = target_len % 256
    r.sendlineafter(b"equivalent password: ", ("B" * needed_len).encode())

    # --- LEVEL 4 ---
    r.recvuntil(b"password is: ")
    desc = r.recvline().decode()
    # Parse "56 'C's + 4 '🔥' emojis."
    c_count = int(re.search(r"(\d+) 'C's", desc).group(1))
    fire_count = int(re.search(r"(\d+) '", desc).group(1)) # Wait, regex might be tricky
    # Let's be more precise
    match = re.search(r"(\d+) 'C's \+ (\d+)", desc)
    c_count = int(match.group(1))
    fire_count = int(match.group(2))
    
    log.info(f"Level 4: {c_count} Cs and {fire_count} Fires")
    
    # Construct full string then truncate to 72 bytes
    # Note: Python handles unicode. We need to truncate BYTES.
    full_str = "C" * c_count + "🔥" * fire_count
    full_bytes = full_str.encode('utf-8')
    
    # Send exactly 72 bytes. 
    # 72 % 256 = 72, so hash processes whole input.
    # Target hash processed full string -> truncated by bcrypt to 72 bytes.
    # So they match.
    payload_bytes = full_bytes[:72]
    r.sendlineafter(b"Enter password: ", payload_bytes)

    # --- LEVEL 5 ---
    r.recvuntil(b"Total Length = ")
    admin_total_len = int(r.recvuntil(b" bytes", drop=True).decode())
    log.info(f"Level 5: Admin total len {admin_total_len}")
    
    prefix = "XCORP_VAULT_ADMIN"
    k = admin_total_len % 256
    
    # We need our (Prefix + Input) to have a length L such that L % 256 == K
    # And (Prefix + Input)[:K] == (Prefix + AdminXs)[:K]
    # Since our input appends to Prefix, the content matches automatically if we just pad with Xs.
    
    current_len = len(prefix)
    
    if k > current_len:
        # If K is larger than prefix, we need to fill up to K
        needed = k - current_len
        payload = "X" * needed
    else:
        # If K is smaller/equal, we need to wrap around to 256 + K
        # e.g. if K=10, we need total length 266. 266 % 256 = 10.
        needed = (256 + k) - current_len
        payload = "X" * needed
        
    r.sendlineafter(b"Input your password:", payload.encode())

    # --- FLAG ---
    r.interactive()

if __name__ == "__main__":
    solve()
```
Flag: PCTF{g00d_v1b3s_b4d_3ntropy_sync72_b4ck1ng}

Solved by: ha1qal

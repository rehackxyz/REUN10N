# Extremely Convenient Breaker

Solved by: @w6rstaimn
### Question:
I won't let you decrypt the flag, but you can use my Extremely Convenient Breaker.
### Solution:
```python
from pwn import *
import ast


def get_dummy(block_index, reference_block):
    dummy = b'\x00' * 16
    if dummy == reference_block:
        dummy = b'\x01' * 16
    return dummy

def build_query(target_index, flag_blocks):
    query_blocks = []
    for i in range(4):
        if i == target_index:
            query_blocks.append(flag_blocks[i])
        else:
            query_blocks.append(get_dummy(i, flag_blocks[i]))
    return b"".join(query_blocks)

def main():
    io = remote("chall.lac.tf", 31180)

    io.recvuntil("Here's the encrypted flag in hex: \n")
    flag_enc_hex = io.recvline().strip().decode()
    log.info("Encrypted flag (hex): %s", flag_enc_hex)

    banner_line = io.recvline().strip().decode()
    log.info("Banner: %s", banner_line)

    io.recvuntil("Enter as hex: ")

    flag_enc = bytes.fromhex(flag_enc_hex)
    if len(flag_enc) != 64:
        log.error("Encrypted flag is not 64 bytes!")
        return

    flag_blocks = [flag_enc[i:i+16] for i in range(0, 64, 16)]
    recovered_flag = b""

    for target_index in range(4):
        query = build_query(target_index, flag_blocks)
        log.info("Sending query for block %d: %s", target_index + 1, query.hex())

        io.sendline(query.hex())

        response = io.recvuntil("Enter as hex: ")
        lines = response.splitlines()
        if not lines:
            log.error("No response received for block %d", target_index + 1)
            break

        decrypted_line = lines[0].decode() if isinstance(lines[0], bytes) else lines[0]
        log.info("Received decrypted line: %s", decrypted_line)

        try:
            decrypted_bytes = ast.literal_eval(decrypted_line)
        except Exception as e:
            log.error("Error parsing decrypted bytes: %s", e)
            break

        recovered_block = decrypted_bytes[target_index * 16:(target_index + 1) * 16]
        log.info("Recovered block %d: %s", target_index + 1, recovered_block.hex())
        recovered_flag += recovered_block

    log.info("Recovered flag (bytes): %s", recovered_flag)
    try:
        log.info("Recovered flag (ascii): %s", recovered_flag.decode())
    except Exception as e:
        log.info("Recovered flag is not valid ASCII: %s", e)

    io.close()

if __name__ == '__main__':
    main()
    #lactf{seems_it_was_extremely_convenient_to_get_the_flag_too_heh}
```

**Flag:** `lactf{seems_it_was_extremely_convenient_to_get_the_flag_too_heh}`
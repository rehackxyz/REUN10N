### Sol  

```
#!/usr/bin/env python3
import sys

unk_493FB = "m7xzr7muqtxsr3m8pfzf6h5ep738ez5ncftss7d1cftskz49qj4zg7n9cizgez5upbzzr7n9cjosg45wqjosg3mu"
aYbndrfg8ejkmcp = "ybndrfg8ejkmcpqxot1uwisza345h769"

def decode_base32_custom(encoded: str, alphabet: str) -> bytes:

    inv_map = {char: idx for idx, char in enumerate(alphabet)}
    output = bytearray()

    for i in range(0, len(encoded), 8):
        block = encoded[i:i+8]
        acc = 0
        for ch in block:
            acc = (acc << 5) | inv_map[ch]
        for shift in (32, 24, 16, 8, 0):
            output.append((acc >> shift) & 0xFF)

    return bytes(output)

def main():
    decoded = decode_base32_custom(unk_493FB, aYbndrfg8ejkmcp)
    password = decoded.decode('utf-8')
    print(password)

if __name__ == "__main__":
    main()
```

```
$ ./whats-a-base
Enter the password:
__rust_begin_short_backtrace__rust_end_short_backtraces
Congratulations! flag{50768fcb270edc499750ea64dc45ee92}
```

Flag:`flag{50768fcb270edc499750ea64dc45ee92}`

Solved by: zeqzoq
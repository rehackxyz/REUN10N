# Crypto - replacement
Solved by **SungJinwoo**\
Full writeup is available here https://sungjinwoo.gitbook.io/wanictf-2024/cryptography

## Question
No one can read my diary!

## Solution
```
import hashlib

def reverse_md5_hash(md5_hash):
    # This function will attempt to find the original integer that, when hashed with MD5, matches md5_hash.
    # Since MD5 is a one-way function, we need to brute force or guess the original number.

    for num in range(256):  # ASCII values range from 0 to 255
        if hashlib.md5(str(num).encode()).hexdigest() == md5_hash:
            return chr(num)
    return None

# Read the encoded data from the file
with open('my_diary_11_8_Wednesday.txt', 'r') as f:
    enc = eval(f.read())

# Decode the list of integers back to characters
decoded_chars = []
for e in enc:
    # Convert integer to hex string and then to MD5 hash
    hex_str = hex(e)[2:]
    # Reverse the MD5 hash to find the original ASCII character
    original_char = reverse_md5_hash(hex_str)
    if original_char:
        decoded_chars.append(original_char)

# Join characters to form the flag
flag = ''.join(decoded_chars)
print("Flag:", flag)
```

### Flag
`FLAG{13epl4cem3nt}`

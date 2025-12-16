https://chat.deepseek.com/share/0qwe7isulgxou8afdr 
```python
# The encrypted string
encrypted = "ufqc~LZI5S6ZR4KA5R!Z=6g3a=`2x"

# Try XOR with single byte keys
for key in range(256):
    decrypted = ''.join(chr(ord(c) ^ key) for c in encrypted)
    if 'flag' in decrypted.lower() or 'ctf' in decrypted.lower():
        print(f"Key {key}: {decrypted}")
```
Flag: pctf{I_L0V3_W1ND0W$_83b6d8e7}

Solved by: ha1qal
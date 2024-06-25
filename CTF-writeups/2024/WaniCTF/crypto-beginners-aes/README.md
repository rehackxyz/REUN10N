# Crypto - beginners_aes
Solved by **SungJinwoo**\
Full writeup available at https://sungjinwoo.gitbook.io/wanictf-2024/cryptography

## Question
AES is one of the most important encryption methods in our daily lives.

## Solution
```
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
import hashlib

# Given encrypted message and hash
enc = b'\x16\x97,\xa7\xfb_\xf3\x15.\x87jKRaF&"\xb6\xc4x\xf4.K\xd77j\xe5MLI_y\xd96\xf1$\xc5\xa3\x03\x990Q^\xc0\x17M2\x18'
flag_hash = '6a96111d69e015a07e96dcd141d31e7fc81c4420dbbef75aef5201809093210e'

# Base key and IV
base_key = b'the_enc_key_is_'
base_iv = b'my_great_iv_is_'

# Brute-force the last byte of the key and IV
for i in range(256):
    key = base_key + bytes([i])
    for j in range(256):
        iv = base_iv + bytes([j])
        try:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_msg = unpad(cipher.decrypt(enc), 16)
            if hashlib.sha256(decrypted_msg).hexdigest() == flag_hash:
                print(f'FLAG = {decrypted_msg.decode()}')
                print(f'Key = {key}')
                print(f'IV = {iv}')
                break
        except (ValueError, KeyError):
            continue
```


### Flag
`FLAG{7h3_f1r57_5t3p_t0_Crypt0!!}`

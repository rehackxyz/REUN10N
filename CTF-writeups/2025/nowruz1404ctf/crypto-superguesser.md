# superguesser
Solved by: @hikki
### Question:
A little guessing, a little crypto. Can you uncover the hidden message?

### Solution:
References from this [article]([https://stackered.com/blog/python-random-prediction/](https://stackered.com/blog/python-random-prediction/ "https://stackered.com/blog/python-random-prediction/"))

```python
r = remote('superguesser.fmc.tf',2001)

r.recvuntil(b' flag: \n')
enc_flag = r.recvline().strip().decode()

print(f'Encrypted flag: {enc_flag}')

rc = RandCrack()



hints = []
for i in range(0,624):
    r.recvuntil(b'Enter an index (0-999): ')
    r.sendline(str(i).encode())
    r.recvuntil(b': ')
    hint = int(r.recvline().strip().decode())
    hints.append(hint)
    # rc.submit(hint)
    # print(f"hint {i}: {hint}")

# print(hints)

encrypted_flag = unhexlify(enc_flag)
for hint in hints:
    rc.submit(hint)
rc.offset(-624)

for i in range(0,100):
    rc.offset(-i)
    predicted_key = rc.predict_getrandbits(128).to_bytes(16, 'big')
    predicted_iv = rc.predict_getrandbits(128).to_bytes(16, 'big')

    try:
        cipher = AES.new(predicted_key, AES.MODE_CBC, predicted_iv)
        decrypted_flag = unpad(cipher.decrypt(encrypted_flag), AES.block_size)

        print(f"Recovered Flag: {decrypted_flag.decode()}")
        print(i)
    except:
        continue
```

**Flag:** `FMCTF{8a78dcb8e926e99a802261bc282aa3af}`
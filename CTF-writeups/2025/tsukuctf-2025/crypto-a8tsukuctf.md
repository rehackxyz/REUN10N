The encryption uses a Vigenère cipher with autokey behavior, where after the initial key, the cipher uses previous ciphertext as the key stream.

Reverse the encryption process by implementing the inverse of `f(p, k)` with  `f_inv(p, k)`

Using a random 8-character key works because the cipher only uses that key for the first 8 characters of the message. After that, it switches to using the previous ciphertext letters as the key. However, we are only able to retrieve the plaintext after the 8th letter this way.

solve.py:

```python
import string

def f_inv(c, k):
    c = ord(c) - ord('a')
    k = ord(k) - ord('a')
    p = (c - k + 26) % 26
    return chr(ord('a') + p)


def decrypt(ciphertext, key):
    assert len(key) <= len(ciphertext)

    idx = 0
    plaintext = []
    cipher_without_symbols = []

    for c in ciphertext:
        if c in string.ascii_lowercase:
            if idx < len(key):
                k = key[idx]
            else:
                k = cipher_without_symbols[idx - len(key)]
            p = f_inv(c, k)
            plaintext.append(p)
            cipher_without_symbols.append(c)
            idx += 1
        else:
            plaintext.append(c)

    return ''.join(plaintext)

cipher="ayb wpg uujmz pwom jaaaaaa aa tsukuctf, hj vynj? mml ogyt re ozbiymvrosf bfq nvjwsum mbmm ef ntq gudwy fxdzyqyc, yeh sfypf usyv nl imy kcxbyl ecxvboap, epa 'avb' wxxw unyfnpzklrq."
key = "aaaaaaaa"

plain = decrypt(cipher, key)
print(plain)
```

Output:
```ayb wpg uujoy this problem or tsukuctf, or both? the flag is concatenate the seventh word in the first sentence, the third word in the second sentence, and 'fun' with underscores.```

Flag: `TsukuCTF25{tsukuctf_is_fun}`

Solved by: ukyovis
# Lepton

Solved by: @Skill Issue 103 Junior

### Question:
In the final days of Rome’s intellectual golden age, the philosopher **Lucius Isogenius** arrived before the Senate, disheveled, eyes burning with madness.

"I have seen beyond numbers," he proclaimed. "Primes are shackles. Modular arithmetic is a crude tool for simple minds. But I— I have forged a cipher that bends the very fabric of reality!"

The Senate groaned.

"The key exchange is weightless," Isogenius continued. "The transformation exists in a space unseen. There are no inverses, no reductions—only a sequence of isogenies guiding the message through dimensions unknown."

One senator raised a hand. "Lucius, will this work?"

Isogenius laughed. "Work? This system is beyond working. It is untouchable. It is the final encryption."

They let him build it. They let him encrypt the most delicate secrets of Rome. They let him construct his temple of mathematical absurdity. And then, as always, the **Numerii** began their work.

### Solution:
```python
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

key = sha256("0".encode()).digest()  # Known key derived from x = 0
ct_hex = "3a641a40286eb1611870ca1a8609689793153b1f404037d202b36969d18e2bb61f6ff9e2fc12142c1a53e01f7f17dc17"  # The ciphertext you received from the challenge
ct = bytes.fromhex(ct_hex)

cipher = AES.new(key, AES.MODE_ECB)
flag = unpad(cipher.decrypt(ct), 16)
print(flag.decode())
```

**Flag:** `TRX{1_R34lly_1n_l0v3_w17h_crypt0}`
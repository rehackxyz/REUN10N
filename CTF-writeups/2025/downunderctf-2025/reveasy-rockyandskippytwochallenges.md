# Solution: MD5; AES decryption

## rocky (MD5 decrypt)
```
crackstation.net
MD5: 70924d0cf669f9d23ccabd561202351f
Decrypted string (payload): emergencycall911
```
Flag: `DUCTF{In_the_land_of_cubicles_lined_in_gray_Where_the_clock_ticks_loud_by_the_light_of_day}`

## skippy (AES decryption)

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii

hex_data = "AE27241B7FFD2C8B3265F22AD1B063F0915B6B95DCC0EEC14DE2C563F7715594007D2BC75E5D614E5E51190F4AD1FD21C5C4B1AB89A4A725C5B8ED3CB37630727B2D2AB722DC9333264725C6B5DDB00DD3C3DA6313F1E2F4DF5180D5F3831843"

ciphertext = binascii.unhexlify(hex_data)

# Key and IV (must be bytes)
key = b"skippy_the_bush_"
iv = b"kangaroooooooooo"

cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

print(plaintext.decode())
```
Flag: `DUCTF{There_echoes_a_chorus_enending_and_wild_Laughter_and_gossip_unruly_and_piled}`

Solved by: gr1d_init_
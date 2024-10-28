# memory-puzzle

Solved by: @n3r

## Question:
The Consortium has concealed a critical file within a memory dump, protected by layers of digital obfuscation. Led by Simon Letti, participants must sift through the volatile memory landscape to locate a plaintext key that unlocks the encrypted file. Time is of the essence, as Roko's Basilisk threatens to distort the data with each passing moment. Can you unravel the puzzle before the Basilisk intervenes?

"Basilisk's whisper will not wait" echos through your mind as you enter the file.

(Note: If you choose to use volatility2.6, use profile Win10x64_19041)

## Solution:
1. use volatility to dump system_update.exe (suspicious because its in user's desktop)
2. decompile the file
3. reverse the encryption method (aes-128-cbc) with the key `SuperSecretKey12`
```
from Crypto.Cipher import AES

key = b"SuperSecretKey12"  
iv = b"\x00" * 16          )

with open("flag.enc", "rb") as enc_file:
    encrypted_data = enc_file.read()

cipher = AES.new(key, AES.MODE_CBC, iv)

decrypted_data = cipher.decrypt(encrypted_data)

padding_length = decrypted_data[-1]
decrypted_data = decrypted_data[:-padding_length]

with open("flag_decrypted.txt", "wb") as dec_file:
    dec_file.write(decrypted_data)

print("Decryption completed. Check 'flag_decrypted.txt' for the output.")
```

**Flag:** `NICC{S1m0n_Tr4v3rses_T1m3}`

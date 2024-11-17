# TriForce Recon

Solved by: @OS1R1S

## Question:
you have intercepted a classified message that has been divided into three encrypted executables and were each hidden on different operating systems.

Flag format:` INTGRITI{Flag1+Flag2+Flag3}``
## Solution:

Flag1
```
def hex_to_string(hex_input):
    return bytes.fromhex(hex_input)

def xor_encrypt(input_data, key):
    return bytes([input_data[i] ^ ord(key[i % len(key)]) for i in range(len(input_data))])

hex_string = "7e54595f09434b0f4a5d59757b514a5b6d550d0f0c765b7d45"
key = "8"

encrypted_data = hex_to_string(hex_string)

original_passphrase = xor_encrypt(encrypted_data, key)

print("Decoded passphrase:", original_passphrase.decode())
#Flag1{s7reaMCircUm574NcE}
```

Flag2
```
def xor_encrypt(a1, a2, a3, a4):
    i = 0
    while i < a4:
        v4 = a1[i]
        a2[i] = ord(a3[i % len(a3)]) ^ v4
        i += 1
    return i

def hex_to_string(hex_str):
    byte_array = bytearray()
    for i in range(0, len(hex_str), 2):
        byte_array.append(int(hex_str[i:i+2], 16))
    return bytes(byte_array)

hex_string = "775a5051034d5644706002635f467d0570030558454b"
xor_key = "16"


encrypted_bytes = hex_to_string(hex_string)

decrypted_bytes = bytearray(len(encrypted_bytes))
xor_encrypt(encrypted_bytes, decrypted_bytes, xor_key, len(encrypted_bytes))

decrypted_flag = decrypted_bytes.decode('utf-8', errors='ignore')
print("flag:", decrypted_flag)
#Flag2{grAV3UnpL3A54nt}
```

Flag3
```
import binascii

def hex_to_string(hex_string):
    byte_array = bytearray()
    for i in range(0, len(hex_string), 2):
        byte_array.append(int(hex_string[i:i+2], 16))
    return byte_array

def xor_decrypt(encrypted_data, key):
    key_len = len(key)
    decrypted_data = bytearray(len(encrypted_data))
    for i in range(len(encrypted_data)):
        decrypted_data[i] = encrypted_data[i] ^ key[i % key_len]
    return decrypted_data

def main():
    encoded_hex = "755e525500496177065b057c076602025d6152467a0755735046025d5d4f"
    encoded_data = hex_to_string(encoded_hex)
    print("Encoded Data:", encoded_data)

    key = b"32"  #key in v6

    decrypted_data = xor_decrypt(encoded_data, key)
    passphrase = decrypted_data.decode('utf-8')

    print("Decoded Passphrase:", passphrase)

if __name__ == "__main__":
    main()
#Flag3{RE5i6N4T10nSatI5fAct1on}
```

**Flag:** `INTGRITI{s7reaMCircUm574NcEgrAV3UnpL3A54ntRE5i6N4T10nSatI5fAct1on}`

Encrypting script and ciphertext is transferred over FTP (captured in pcap), it's a substitution cipher.

```python
#!/usr/bin/env python3
import sys

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def shift_chars(text, pos):
    out = ""
    for letter in text:
        if letter in alphabet:
            letter_pos = (alphabet.find(letter) - pos) % 26  # subtract for decrypt
            new_letter = alphabet[letter_pos]
            out += new_letter
        else:
            out += letter
    return out

def decrypt_text(text):
    counter = 0
    decrypted_text = ""
    for i in range(0, len(text), 10):
        counter = (counter + 1) % 26
        decrypted_text += shift_chars(text[i:i+10], counter)
    return decrypted_text

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <encrypted_file>")
        sys.exit(1)

    filename = sys.argv[1]

    with open(filename, "r") as f:
        encrypted_data = f.read()

    decrypted_data = decrypt_text(encrypted_data)

    with open(f"{filename}.decrypted", "w") as f:
        f.write(decrypted_data)

    print(f"Decrypted text written to {filename}.decrypted")
```

Flag: `flag{ad1c53bf1e00a9239d29edaadcda2964}`

Solved by: benkyou
# too-loud-to-yap

Solved by: @w6rstaimn
### Question:
AAAAA

i love AAAAA telling and posting stories! you could AAAAA say its something of a heritage for me :3

unfortunately, when i AAAAA tried telling this story about "autos", some guy kept YELLING "AAAAA" in the background which AAAAA kept messing up my new take on the vigenere cipher! he actually started yelling right AAAAA when i started my story :( weh...
### Solution:
```python
import re

def autokey_decrypt(ciphertext, keyseed="autos"):
    key = list(keyseed)
    plaintext = []
    key_index = 0
    
    for char in ciphertext:
        if char.isalpha() and char.islower():
            c_val = ord(char) - ord('a')
            k_val = ord(key[key_index]) - ord('a')
            p_val = (c_val - k_val) % 26
            p_char = chr(p_val + ord('a'))
            plaintext.append(p_char)
            key.append(p_char)
            key_index += 1
        else:
            plaintext.append(char)
    return "".join(plaintext)

def main():
    with open("ct.txt", "r") as f:
        ct = f.read()
    
    segments = re.split(r'(\b[A-Z]+\b)', ct)
    
    out_parts = []
    for seg in segments:
        if seg.isalpha() and seg.upper() == seg:
            out_parts.append(seg)
        else:
            dec = autokey_decrypt(seg, keyseed="aaaaa")
            out_parts.append(dec)
    
    result = "".join(out_parts)
    print(result)

if __name__ == "__main__":
    main()
```

**Flag:** `lactf{down_with_cis_bus}`
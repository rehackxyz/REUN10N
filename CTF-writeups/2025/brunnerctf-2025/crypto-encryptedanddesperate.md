```
Brunnerne's Royal Court Baker is in a desperate situation. His computer was hit by a ransomware attack that encrypted all his professional brunsviger photos and secret recipes.

The attackers left behind a suspicious ransomware file - it might hold the key to unlock everything, but he doesn't dare touch it without your expert help!```

The files inside `/recipes/` folder are encrypted with a 16 bytes key. Using png and webp header to get the first 12 bytes of the key then manually find another 4 bytes by analysing the png string. (by guessing some familiar strings such as `http://`, `ChatGPT` etc)

```python
from itertools import permutations, cycle
from pathlib import Path

key = bytes.fromhex("268f76ad1431f132879fcb6c0e704b99")
TARGET_DIR = Path("recipes/")

def decrypt_file(file: Path, key: bytes):
    with open(file, "rb") as f:
        ciphertext = f.read()
    plaintext = bytes(c ^ k for c, k in zip(ciphertext, cycle(key)))
    out_file = file.with_suffix("")
    with open(out_file, "wb") as f:
        f.write(plaintext)
    print(f"Decrypted {file.name} -> {out_file.name}")

def main():
    print("Recovered XOR key:", key.hex())

    for file in TARGET_DIR.glob("*.enc"):
        decrypt_file(file, key)

    print("All files decrypted!")

if __name__ == "__main__":
    main()
```

The flag is inside one of the pdf file 
`brunner{mY_pr3c10u5_r3c1p35_U_f0und_7h3m} `

Solved by: ukyovis
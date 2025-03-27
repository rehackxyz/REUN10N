# Solution
```
┌──(myenv)(osiris㉿ALICE)-[~/Downloads/CTF/nullcon/rev/scramble]
└─$ cat sol3.py
import random

def decode_flag(scrambled_result, key, seed):
    chunk_size = 4
    chunks = [scrambled_result[i:i+chunk_size] for i in range(0, len(scrambled_result), chunk_size)]

    random.seed(seed)
    shuffled_indices = list(range(len(chunks)))
    random.shuffle(shuffled_indices)

    unshuffled_chunks = [None] * len(chunks)
    for i, idx in enumerate(shuffled_indices):
        unshuffled_chunks[idx] = chunks[i]

    unshuffled_result = [item for chunk in unshuffled_chunks for item in chunk]

    flag = ''.join([chr(c ^ key) for c in unshuffled_result])
    return flag

def main():
    scrambled_hex = "1e78197567121966196e757e1f69781e1e1f7e736d6d1f75196e75191b646e196f6465510b0b0b57"
    scrambled_result = [int(scrambled_hex[i:i+2], 16) for i in range(0, len(scrambled_hex), 2)]

    key = 42

    for seed in range(11):
        try:
            flag = decode_flag(scrambled_result, key, seed)
            if flag.startswith('ENO{'):
                print(f"Seed: {seed}, Flag: {flag}")
                break
        except Exception as e:
            print(f"Error with seed {seed}: {e}")
            continue

if __name__ == "__main__":
    main()

┌──(myenv)(osiris㉿ALICE)-[~/Downloads/CTF/nullcon/rev/scramble]
└─$ python sol3.py
Seed: 10, Flag: ENO{5CR4M83L3D_3GG5_4R3_1ND33D_T45TY!!!}
```

Flag: `ENO{5CR4M83L3D_3GG5_4R3_1ND33D_T45TY!!!}`


Solved by: OS1R1S

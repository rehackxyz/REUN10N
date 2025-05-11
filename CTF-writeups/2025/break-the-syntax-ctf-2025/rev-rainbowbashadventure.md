# Solution
Go to `RenPy` source file, we need to find shortest path to traverse all 19 cloud. Start at `cloud0`, always fly to the closest unvisited cloud, and repeat until all clouds are visited. Then return to `cloud0`.

When you get the correct path, then you can decode the flag.
```
import hashlib

flag = b""

def xor(target, key):
    out = [c ^ key[i % len(key)] for i, c in enumerate(target)]
    return bytearray(out)

def key_from_path(path):
    return hashlib.sha256(str(path).encode()).digest()

def check_path(path, enc_flag):
    global flag
    flag1 = xor(enc_flag, key_from_path(path))
    flag2 = xor(enc_flag, key_from_path(list(reversed(path))))
    if flag1.startswith(b"BtSCTF"):
        flag = flag1
        print(flag)
        flag = bytes(flag).replace(b"{", b"{{").decode('ascii')
        return True
    if flag2.startswith(b"BtSCTF"):
        flag = flag2
        print(flag)
        flag = bytes(flag).replace(b"{", b"{{").decode('ascii')
        return True
    return False

# 👉 Replace with the path you found:
nodes = [0, 12, 15, 2, 1, 5, 11, 14, 17, 7, 19, 13, 9, 10, 3, 8, 16, 18, 4, 6, 0]  # <- Example path; use your actual solution

is_correct = check_path(nodes, bytearray(b'\xc2\x92\xf9\xf66\xe8\xa5\xa6\x17\xb6mGE\xcfQ\x90Mk:\x9a\xbb\x905&\x19\x8e\xc4\x9a\x0b\x1f\xf8C\xf4\xb9\xc9\x85R\xc2\xbb\x8d\x07\x94[R_\xf5z\x9fAl\x11\x9c\xbb\x9255\x08\x8e\xf6\xd6\x04'))

if is_correct:
    print("all cloudz smashed im the queen")
    print("i got 100% swag")
    print(flag)
else:
    print("Sadly, Rainbom Bash was too slow and wasn't able to smash all clouds.")

```

Flag: BtSCTF{YOU_are_getting_20_percent_c00ler_with_this_one_!!_B)}


Solved by: arifpeycal

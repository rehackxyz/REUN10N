# Solution
```└─$ cat sol.py
def rev(e):
    return bytes(((b << 5 & 0xFF | b >> 3) - i & 0xFF) ^ 0x5A for i, b in enumerate(e))

e = [248,168,184,33,96,115,144,131,128,195,155,128,171,9,89,211,33,211,219,216,251,73,153,224,121,60,76,73,44,41,204,212,220,66]

print(rev(e).decode())```

Flag: `ENO{R3V3R53_3NG1N33R1NG_M45T3R!!!`


Solved by: OS1R1S

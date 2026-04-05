# rev - README.pdf

```
expected = [46,49,56,57,46,60,33,16,110,44,110,9,57,40,107,42,46,5,107,52,5,10,30,28,39]
k = 90

flag = "".join(chr(x ^ k) for x in expected)
print(flag)
```

Flag:`tkbctf{J4v4Scr1pt_1n_PDF}`

Compiled by: yappare
Solved by: g10d
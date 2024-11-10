# Training Problem: Intro to Reverse

Solved by: @OS1R1S

## Question:
Just a classic flagchecker.


## Solution:
```
v5 = "ucaqbvl,n*d\\'R#!!l"
decoded = ''.join(chr(ord(v5[i]) + i) for i in range(18))
print(decoded)

#udctf{r3v3ng3_101}
```

**Flag:`udctf{r3v3ng3_101}`** 

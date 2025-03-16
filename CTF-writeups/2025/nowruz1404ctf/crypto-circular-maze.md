# Circular Maze

### Question:
you got plenty of information, now get crackin!!

### Solution:
Here is the solution script for the challenge
```python
import string

with open("circular-maze/flag.enc", "rb") as f:
    encrypted_flag = list(f.read())

flag = list("FMCTF{")
flag_length = len(encrypted_flag)

def encrypt(data, i):
    return (ord(data[i - 1]) + ord(data[i]) + ord(data[(i + 1) % flag_length])) % 256

while len(flag) < flag_length - 1:
    for char in string.printable:
        test_flag = flag + [char] + ["_"] * (flag_length - len(flag) - 1) 
        # print((test_flag))
        guess = ''.join(test_flag)
        print(guess)
        if encrypt(guess, (len(flag) - 1)) == encrypted_flag[len(flag)-1]: 
            flag.append(char) 
            # print(flag)
            break


flag.append("}")  

flag_str = "".join(flag)
print("Recovered flag:", flag_str)
```

**Flag:** `FMCTF{broken_circle_is_not_fun_at_all}`
# Extended 

Solved by: @yappare
### Question:
What if I took my characters and... extended them?
### Solution:

```python
# Read the content of chall.txt
with open("chall.txt", "rb") as f:
    encoded_flag = f.read().decode("iso8859-1")

original_flag = ""

for c in encoded_flag:
    # Convert the character to its 8-bit binary representation
    o = bin(ord(c))[2:].zfill(8)
    
    # Replace the first 1 with a 0
    for i in range(8):
        if o[i] == "1":
            o = o[:i] + "0" + o[i + 1:]
            break
    
    # Convert the modified binary string back to a character
    original_flag += chr(int(o, 2))

print(original_flag)
```

**Flag:** `lactf{Funnily_Enough_This_Looks_Different_On_Mac_And_Windows}`


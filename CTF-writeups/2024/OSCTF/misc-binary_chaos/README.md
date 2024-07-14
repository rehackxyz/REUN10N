# Binary Chaos
Solved by **6E3372**

## Question
My friend sent me this weird binary and claims that he used some kind of encryption on this? Can you reveal the malicious intentions of my friend sending this to me?

## Solution
decode the binary using binaryfuck, then you will get flag char and indices

```
flag_chars = ['B', '4', '{', 'c', 'F', '}', '_', 'K', 'n', 'F', 'T', 'O', 'S', '1', 'C', 'r', '#', 'y']
indices = [11, 14, 5, 8, 4, 17, 10, 9, 13, 4, 3, 0, 1, 12, 2, 15, 7, 16]
def arrange_flag(chars, idxs):
    flag = [''] * len(chars)
    for i, idx in enumerate(idxs):
        flag[idx] = chars[i]
    return ''.join(flag)
print(arrange_flag(flag_chars, indices))
```
### Flag
`OSCTF{XXX}`

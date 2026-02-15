# rev - k

```
h = [205, 196, 215, 218, 225, 226, 1189, 2045, 2372, 9300, 8304, 660,
     8243, 16057, 16113, 16057, 16004, 16007, 16006, 8561, 805, 346,
     195, 201, 154, 146, 223]

# The loop uses h[0..25] (last element h[26] is unused)
prefix = "lactf{"
c0 = ord(prefix[0])  # 'l'

codes = [c0]
for i in range(len(h) - 1):  # 26 equations -> 27 chars
    codes.append(h[i] - codes[i])

flag_core = "".join(chr(x) for x in codes)

print("Recovered (checked) string:", flag_core)
print("Suggested final flag:", flag_core + "}")
```
Flag:` lactf{gоοօỏơóὀόὸὁὃὄὂȯöd_j0b}`

Solved by: yappare
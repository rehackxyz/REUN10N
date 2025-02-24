Solved by: @w6rstaimn

### Question:
Let's make a promise that on that day, when we meet again, you'll take the time to tell me the flag.

_You have no more unread messages from LA CTF._
### Solution:
```python
def solve(n, target):
    steps = 0
    while steps < target:
        if n % 2 == 0:
            n //= 2
        else:
            n = n * 3 + 1
        steps += 1
        if n == 1 and steps < target:
            return -1
    return n

yin = [0x1B, 0x26, 0x57, 0x5f , 0x76, 0x9]
access_code = ""

for t in yin:
    for c in range(0x20, 0x7F):
        if solve(c, t) == 1:
            access_code += chr(c)
            found = True
            print(f"Target {t}: Found character {chr(c)} ({c})")
            break
    if not found:
        print("No found =", t)
        break

print("Access code is:", access_code)
```

**Flag:** `lactf{the_only_valid_solution_is_BigyaP}`
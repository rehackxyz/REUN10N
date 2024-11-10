# 🅱️rainrot.c

Solved by: @ks

## Question:
I would like to apologize for the crimes that have been committed upon humanity and the mental trauma that may ensue from the creation of this code. I take full responsibility for my actions and ask only for forgiveness as you struggle in pursuit of the flag. I have provided C source code and omitted the header that serves as the gen-z Rosetta Stone. I wish you all the best in successful completion of this problem.

## Solution:
- basically convert all the weird thing into something readable and then satisfy each criteria one by one. @ks replaced them manually.

```
from z3 import *

# Create a list of 51 BitVec variables for each character in the flag
flag = [BitVec(f'flag_{i}', 8) for i in range(51)]
solver = Solver()

# Rule 0: The flag must be exactly 51 characters long
solver.add(flag[50] != 0)  # 51st character exists

# Rule 1: The flag must start with "udctf"
for i, c in enumerate("udctf"):
    solver.add(flag[i] == ord(c))

# Rule 2: The flag must end with '}'
solver.add(flag[50] == ord('}'))

# Rule 3: Specific character arithmetic check (this result should be '{' but i dunno why z3 doesnt work that way)
solver.add((flag[5] * 4) % 102 == ord('T'))

# Rule 4: Bitwise AND of two characters must equal 0x69
solver.add((flag[35] & flag[33]) == 0x69)

# Rule 5: Characters at positions 6 and 31 must be equal
solver.add(flag[6] == flag[31])

# Rule 6: Sum of characters at positions 31 and 35 equals double of character at position 6
solver.add(flag[31] + flag[35] == 2 * flag[6])

# Rule 7: Three pairs of characters must be equal
solver.add(flag[7] == flag[10])
solver.add(flag[14] == flag[23])
solver.add(flag[28] == flag[36])

# Rule 8: Multiple character equality checks
solver.add(flag[42] == flag[28])
solver.add(flag[36] == flag[23])
solver.add(flag[10] == flag[42])

# Rule 9: Character at position 10 must be '_'
solver.add(flag[10] == ord('_'))

# Rule 10-12: XOR transformations and comparisons
key = [0x47, 0x4A, 0x13, 0x42, 0x58, 0x57, 0x1B]

# Rule 10: XOR on positions 29-35 should equal "r!zz13r"
for i, c in enumerate("r!zz13r"):
    solver.add(flag[29 + i] ^ key[i] == ord(c))

# Rule 11: XOR on positions 43-49 should equal "5ki8idi"
for i, c in enumerate("5ki8idi"):
    solver.add(flag[43 + i] ^ key[i] == ord(c))

# Rule 12: XOR on positions 15-22 with the transformed2 pattern
transformed2 = [ord('5'), ord('k'), ord('i'), ord('8'), ord('i'), ord('d'), ord('i')]
target_str = [0x40, 0x05, 0x5C, 0x48, 0x59, 0x0F, 0x5A, 0x5B]
for i in range(8):
    solver.add(flag[15 + i] ^ transformed2[i % 7] == target_str[i])

# Rule 13: Bitwise AND must equal '0'
solver.add((flag[24] & flag[19]) == ord('0'))

# Rule 14: Bitwise OR must equal '0'
solver.add((flag[24] | flag[27]) == ord('0'))

# Rule 15: Characters at positions 26 and 44 must be equal
solver.add(flag[26] == flag[44])

# Rule 16: Increment characters and compare to target
target_incremented = [0x62, 0x6E, 0x60, 0x75, 0x69, 0x34]
for i in range(6):
    solver.add(flag[8 + i] + 1 == target_incremented[i])

# Rule 17: XOR transformation and comparison
target_transformed = [0x05, 0x17, 0x01, 0x01, 0x1D]
for i in range(5):
    solver.add((flag[37 + i] ^ target_incremented[i]) == target_transformed[i])

# Check if a solution exists and print the flag with unknowns as "?"
if solver.check() == sat:
    model = solver.model()
    flag_str = ''.join(
        chr(model[flag[i]].as_long()) if model[flag[i]] is not None else '?' 
        for i in range(51)
    )
    print(f"Solved flag (with unknowns as '?'): {flag_str}")
else:
    print("No solution found.")

## the script somehow getting 50 chars instead of 51 chars I dunno why.
## the flag should be `udctf{i_am_th3_un5p0k3n_0h!0_5ki8idi_gyatt_r!zz13r}`
## if you see carefully the `0h!0` will become 3 chars only in this script, i dunno whats wrong with it
## the `h` I literally guessed it since there's no any criteria that fulfill this 
```
**Flag:`udctf{i_am_th3_un5p0k3n_0h!0_5ki8idi_gyatt_r!zz13r}`** 

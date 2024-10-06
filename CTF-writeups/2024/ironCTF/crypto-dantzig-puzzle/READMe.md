# Dantzig's Puzzle

Solved by: @hikki

## Question:

Dantzig was on a trip with his friends and one day, they decided to play a game or atleast, it's easier version. He would think of a string and the others have to find it based on the clues he gives them.

1. The knapsack list contains 8 numbers, with 1 and 2 as the first two numbers and the subsequent numbers are formed by adding one to the sum of all the numbers before.
2. The value of m=257 and n is something less than 257
3. The encrypted string is - [538, 619, 944, 831, 360, 531, 468, 971, 635, 593, 655, 425, 1068, 530, 1068, 360, 706, 1068, 299, 619, 670, 1068, 891, 425, 670, 1068, 371, 670, 732, 531, 1068, 484, 372, 635, 371, 372, 237, 237, 1007]

Can you find the string Dantzig was thinking of?

Flag Format: ironCTF{this\_is\_fake}

## Solution:

```py
from sympy import mod_inverse

knapsack = [1, 2, 4, 8, 16, 32, 64, 128]

m = 257

ciphertext = [538, 619, 944, 831, 360, 531, 468, 971, 635, 593, 655, 425, 
              1068, 530, 1068, 360, 706, 1068, 299, 619, 670, 1068, 891, 
              425, 670, 1068, 371, 670, 732, 531, 1068, 484, 372, 635, 
              371, 372, 237, 237, 1007]

def solve_knapsack(value, knapsack):

    binary_representation = []
    for weight in reversed(knapsack):
        if weight <= value:
            binary_representation.append(1)
            value -= weight
        else:
            binary_representation.append(0)
    return list(reversed(binary_representation))

for n in range(1, 257):
    try:
        n_inverse = mod_inverse(n, m)
    except ValueError:
        continue
    
    transformed_values = [(c * n_inverse) % m for c in ciphertext]
    
    decoded_bits = []
    for value in transformed_values:
        bits = solve_knapsack(value, knapsack)
        decoded_bits.extend(bits)
    
    try:
        decoded_message = ''.join(chr(int(''.join(map(str, decoded_bits[i:i+8])), 2)) for i in range(0, len(decoded_bits), 8))
        
        if all(32 <= ord(char) <= 126 for char in decoded_message):
            print(f"Possible decrypted message with n = {n}: {decoded_message}")
    
    except ValueError:
        continue

```

**Flag:** `ironCTF{M4th_&_C5_ar3_7h3_b3sT_c0Mb0!!}`




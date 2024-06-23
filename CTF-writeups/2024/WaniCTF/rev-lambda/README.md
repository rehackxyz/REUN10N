# Rev - Lambda
Solved by **ks**

## Question
Let's dance with lambda!

## Solution
```
# Encoded target string
encoded_target = '16_10_13_x_6t_4_1o_9_1j_7_9_1j_1o_3_6_c_1o_6r'

# Function to decode the encoded string
def decode(encoded_str):
    return ''.join(chr(int(c, 36) + 10) for c in encoded_str.split('_'))

# Function to apply reverse transformations
def reverse_transform(input_str):
    # Reverse of Transform 3: XOR with 123
    step1 = ''.join(chr(123 ^ ord(c)) for c in input_str)
    # Reverse of Transform 2: shift characters +3
    step2 = ''.join(chr(ord(c) + 3) for c in step1)
    # Reverse of Transform 1: shift characters -12
    return ''.join(chr(ord(c) - 12) for c in step2)

# Decode the target and apply the reverse transformations
decoded_target = decode(encoded_target)
original_flag = reverse_transform(decoded_target)

# Print the original flag
print("Original Flag:", original_flag)
```

### Flag
`FLAG{}`

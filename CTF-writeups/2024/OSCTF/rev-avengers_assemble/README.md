# Avengers assemble 
Solved by **vicevirus**

## Question
The Avengers have assembled but for what? To solve this!? Why call Avengers for such a simple thing, when you can solve it yourself

FLAG FORMAT: OSCTF{Inp1_Inp2_Inp3} (Integer values)

## Solution
```
required_sum = 0xDEADBEEF
condition_inp2 = 0x6F56DF8D
xor_result = 2103609845  # 0x7D5DF85D

inp1 = required_sum - condition_inp2

if inp1 > 0x6F56DF65:
    raise ValueError(f"Calculated inp1 value {inp1} exceeds the allowed maximum value.")

inp3 = xor_result ^ condition_inp2


print(f"OSCTF{{{inp1}_{condition_inp2}_{inp3}}}")

print(f"inp1: {inp1} (hex: {hex(inp1)})")
print(f"inp2: {condition_inp2} (hex: {hex(condition_inp2)})")
print(f"inp3: {inp3} (hex: {hex(inp3)})")
```

### Flag
`OSCTF{1867964258_1867964301_305419896}`

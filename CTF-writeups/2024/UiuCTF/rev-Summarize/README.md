# Rev - Summarize
Solved by **Identities**

## Question
All you have to do is find six numbers. How hard can that be?

## Solution
* understand all the obfuscated mathematical operations (total of 5 operations: bitwise xor, bitwise and, add, subtract and multiply)
* create z3 script based on the obfuscated functions
* 
```
from z3 import *

# Define the Z3 solver
solver = Solver()

# Define symbolic variables for param_1 to param_6
param_1 = BitVec('param_1', 32)
param_2 = BitVec('param_2', 32)
param_3 = BitVec('param_3', 32)
param_4 = BitVec('param_4', 32)
param_5 = BitVec('param_5', 32)
param_6 = BitVec('param_6', 32)

# Add constraints based on the function FUN_0040137b
solver.add(param_1 >= 0x5f5e101)
solver.add(param_2 >= 0x5f5e101)
solver.add(param_3 >= 0x5f5e101)
solver.add(param_4 >= 0x5f5e101)
solver.add(param_5 >= 0x5f5e101)
solver.add(param_6 >= 0x5f5e101)

solver.add(param_1 < 1000000000)
solver.add(param_2 < 1000000000)
solver.add(param_3 < 1000000000)
solver.add(param_4 < 1000000000)
solver.add(param_5 < 1000000000)
solver.add(param_6 < 1000000000)

uVar1 = param_1 - param_2
uVar2 = uVar1 + param_3
uVar3 = param_1 + param_2
uVar1 = param_2 * 2
uVar4 = 3 * param_1
uVar5 = uVar4 - uVar1
uVar6 = param_1 ^ param_4
uVar1 = param_3 + param_1
uVar7 = param_2 & uVar1
uVar11 = param_2 + param_4
uVar1 = param_4 + param_6
uVar8 = param_3 ^ uVar1
uVar9 = param_5 - param_6
uVar10 = param_5 + param_6

# Adjust the condition to handle bit-vector sizes correctly
cond = ((uVar11 & 0xffffffff) % param_1) == 0x2038c43c

solver.add(uVar2 % 0x10ae961 == 0x3f29b9)
solver.add(uVar3 % 0x1093a1d == 0x8bdcd2)
solver.add(uVar5 % uVar6 == 0x212c944d)
solver.add(uVar7 % 0x6e22 == 0x31be)
solver.add(cond)
solver.add(uVar8 % 0x1ce628 == 0x1386e2)
solver.add(uVar9 % 0x1172502 == 0x103cf4f)
solver.add(uVar10 % 0x2e16f83 == 0x16ab0d7)

# Check satisfiability
if solver.check() == sat:
    model = solver.model()
    param1_val = model[param_1].as_long()
    param2_val = model[param_2].as_long()
    param3_val = model[param_3].as_long()
    param4_val = model[param_4].as_long()
    param5_val = model[param_5].as_long()
    param6_val = model[param_6].as_long()
    
    print(f"param_1 = {param1_val}")
    print(f"param_2 = {param2_val}")
    print(f"param_3 = {param3_val}")
    print(f"param_4 = {param4_val}")
    print(f"param_5 = {param5_val}")
    print(f"param_6 = {param6_val}")
else:
    print("No solution found.")
```

### Flag
`uiuctf{2a142dd72e87fa9c1456a32d1bc4f77739975e5fcf5c6c0}`

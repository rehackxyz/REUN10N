# lists of JSONs

Solved by: @vicevirus

## Question:
Web...ish...

On the web contains:
```
FLAG FORMAT: UDCTF{}
CHR: ? NEXTCHR: 1627 - 1151
CHR: 3 NEXTCHR: 275 + 896
CHR: O NEXTCHR: 912660 / 2173
CHR: } NEXTCHR: 5918500 / 3115
CHR: . NEXTCHR: -88 + 713
```

## Solution:

list of jsons

`https://lists-of-jsons-default-rtdb.firebaseio.com/.json`

```
import json
import re

def evaluate_expression(expr):
    """
    Safely evaluate a mathematical expression and return the result.
    Supports basic arithmetic operations.
    """
    # Remove all whitespace
    expr = expr.replace(' ', '')
    
    # Check for exit condition
    if expr.lower() == "exit()":
        return "exit"
    
    # Define allowed characters (digits and arithmetic operators)
    if not re.match(r'^[\d\+\-\*\/\(\)]+$', expr):
        raise ValueError(f"Invalid characters in expression: {expr}")
    
    try:
        # Evaluate the expression
        result = eval(expr)
        return int(result)
    except Exception as e:
        raise ValueError(f"Error evaluating expression '{expr}': {e}")

def extract_flag(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    flag = ""
    visited = set()
    current_index = 0
    
    while True:
        if current_index in visited:
            print(f"Detected a loop at index {current_index}. Terminating traversal.")
            break
        if current_index < 0 or current_index >= len(data['flag']):
            print(f"Index {current_index} is out of bounds. Terminating traversal.")
            break
        
        current_obj = data['flag'][current_index]
        chr_val = current_obj.get('chr', '')
        next_val = current_obj.get('next', '')
        
        # Termination conditions
        if chr_val == "END":
            print("Reached END. Terminating traversal.")
            break
        if not chr_val:
            print(f"No 'chr' value at index {current_index}. Terminating traversal.")
            break
        
        flag += chr_val
        visited.add(current_index)
        
        # Evaluate the 'next' expression
        try:
            next_index = evaluate_expression(next_val)
            if next_index == "exit":
                print("Encountered 'exit()'. Terminating traversal.")
                break
            current_index = next_index
        except ValueError as ve:
            print(f"Error: {ve}. Terminating traversal.")
            break
    
    return flag

if __name__ == "__main__":
    json_file = 'bro.json'  # Replace with your JSON file path
    flag = extract_flag(json_file)
    print(f"Extracted Flag: {flag}")
```
**Flag:`UDCTF{JS0N_1n_tr33}`** 

# Emoji Stack

Solved by: @okay

- Category: misc
- Description: 
```
Welcome to Emoji Stack, the brand new stack based emoji language! Instead of other stack based turing machines that use difficult to read and challenging characters like + - and [], Emoji Stack uses our proprietary patent pending emoji system.

The details of our implentation is below:

👉: Move the stack pointer one cell to the right
👈: Move the stack pointer one cell to the lef
👍: Increment the current cell by one, bounded by 255
👎: Decrement the current cell by one, bounded by 0
💬: Print the ASCII value of the current cell
🔁##: Repeat the previous instruction 0x## times
The Emoji Stack is 256 cells long, with each cell supporting a value between 0 - 255.

As an example, the program "👍🔁47💬👉👍🔁68💬👉👍🔁20💬" Would output "Hi!" with the following execution flow:

[0, 0, 0, 0] 👍🔁47

[0x48, 0, 0, 0] 💬👉: H

[0x48, 0, 0, 0] 👍🔁68

[0x48, 0x69, 0, 0] 💬👉: i

[0x48, 0x69, 0, 0] 👍🔁20

[0x48, 0x69, 0x21, 0] 💬: !
```
Flag format: CACI{.\*}

- Challenge File: input.txt



### Solutions:

```py
 RIGHT = ':point_right:'
LEFT = ':point_left:'
INC = ':thumbsup:'
DEC = ':thumbsdown:'
PRINT = ':speech_balloon:'
REPEAT = ':repeat:'

stack = [0] * 256
pointer = 0

with open('input.txt', 'r', encoding='utf-8') as file:
    code = file.read()

i = 0  
while i < len(code):
    instruction = code[i]
    
    if instruction == RIGHT:
        pointer = (pointer + 1) % 256  
    elif instruction == LEFT:
        pointer = (pointer - 1) % 256  
    elif instruction == INC:
        stack[pointer] = (stack[pointer] + 1) % 256  
    elif instruction == DEC:
        stack[pointer] = (stack[pointer] - 1) % 256  
    elif instruction == PRINT:
        print(chr(stack[pointer]), end="")
    elif instruction == REPEAT:
        repeat_count = int(code[i + 1:i + 3], 16)  
        previous_instruction = code[i - 1]  

        for _ in range(repeat_count):
            if previous_instruction == RIGHT:
                pointer = (pointer + 1) % 256
            elif previous_instruction == LEFT:
                pointer = (pointer - 1) % 256
            elif previous_instruction == INC:
                stack[pointer] = (stack[pointer] + 1) % 256
            elif previous_instruction == DEC:
                stack[pointer] = (stack[pointer] - 1) % 256
            elif previous_instruction == PRINT:
                print(chr(stack[pointer]), end="")
        i += 2  
    
    i += 1
```

**Flag:** `CACI{TUR!NG_!5_R011!NG_!N_H!5_GR@V3}`


# misc - iUseArchBTW??

https://github.com/overmighty/i-use-arch-btw 

the encryption method use brainfuck. crafting new pattern using this info instead of downloading the whole project:
https://github.com/overmighty/i-use-arch-btw/blob/master/docs/language_specification.md

```
# Read the file
with open("arch.archbtw", "r") as f:
    code = f.read().split()

# Map keywords to Brainfuck commands
bf_map = {
    "i": ">",
    "use": "<",
    "arch": "+",
    "linux": "-",
    "btw": ".",
    "by": ",",
    "the": "[",
    "way": "]",
}

# Convert to Brainfuck code
bf_code = "".join(bf_map[word] for word in code if word in bf_map)

# Brainfuck interpreter
def run_bf(code):
    tape = [0] * 30000
    ptr = 0
    i = 0
    stack = []
    while i < len(code):
        cmd = code[i]
        if cmd == ">":
            ptr += 1
        elif cmd == "<":
            ptr -= 1
        elif cmd == "+":
            tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == "-":
            tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == ".":
            print(chr(tape[ptr]), end="")
        elif cmd == ",":
            tape[ptr] = ord(input()[0])
        elif cmd == "[":
            if tape[ptr] == 0:
                open_brackets = 1
                while open_brackets:
                    i += 1
                    if code[i] == "[":
                        open_brackets += 1
                    elif code[i] == "]":
                        open_brackets -= 1
            else:
                stack.append(i)
        elif cmd == "]":
            if tape[ptr] != 0:
                i = stack[-1]
            else:
                stack.pop()
        i += 1

# Run the program
run_bf(bf_code)
```

Flag:`0xL4ugh{1_us3_4rch_l1nux_btw_4nd_y0u_sh0uld_t00_p4cm4n_r0ck5}`

Solved by OS1R1S

Solved by: yappare

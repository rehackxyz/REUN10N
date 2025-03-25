# Solution
Get disassembly from `objdump -d -Mintel uncertain > disassembly.txt`

There is a repeating pattern that moves some value from the flag into eax. Then the lower 8 bits is cmp with a value, since it is 8 bits this is likely an ASCII character. I matched the first few offsets and got ping.
```
movzx    eax, byte ptr [rip + 0x33691] # 0x446040 <flag>
cmp    al, 0x70
```

The disassembly is very long and when I initially did the mapping manually I missed out characters. So, I grepped out each line with `<flag+offset>` and the `cmp` after it. Then we sort the value being cmp with the offset as key, then build the flag.

We also need to change `<flag>` to `<flag+0x0>` for parsing 🙂
```
cat disassembly.txt | grep flag | cut -d"#" -f2 | cut -d" " -f3 > index.txt
cat disassembly.txt | grep flag -a1 | grep cmp | cut -d "," -f2 | sed "s/ //g" > values.txt
```

Script:
```
import itertools

with open("index.txt", "r") as f:
    index = [line.strip() for line in f.readlines()]

with open("values.txt", "r") as f:
    values = [line.strip() for line in f.readlines()]

offsets = []
for i, line in enumerate(index):
    # Strip the '<flag+' and '>' to get the hex value
    data = line.replace("<flag","").replace(">","")
    # Convert th hex part to an integer
    offset = int(data, 16)
    offsets.append((i, offset))

sorted_data = sorted(offsets, key=lambda x: x[1])

values = [values[i[0]] for i in sorted_data]

def remove_consecutive_duplicates(s):
    return ''.join(ch for ch, _ in itertools.groupby(s))

flag = []
for line in values:
    flag.append(line)

s = "".join([chr(int(c,16)) for c in flag])
cleaned_string = remove_consecutive_duplicates(s)
print(cleaned_string)
```

Flag: `ping{S0_much_IF5_17_1s_4lm057_A1}`

Solved by: yappare
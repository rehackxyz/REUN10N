```
output = [output.txt content]

first_val = 5
second_val = 6

length = len(output)
half = length // 2

second = output[:half]
first = output[half:]

first_half = []
for val in first:
    char = (~(val ^ first_val)) & 0xFF
    first_half.append(chr(char))

second_half = []
for val in second:
    char = (~(val ^ second_val)) & 0xFF
    second_half.append(chr(char))

art_str = ''.join(first_half) + ''.join(second_half)

art_list = list(art_str)
flag_chars = []
i = len(art_list) % 10
flag_track = 0

while i < len(art_list) and flag_track < 100:
    flag_chars.append(art_list[i])
    i += 28
    flag_track += 1

flag = ''.join(flag_chars)
print(flag)
```

Flag: pctf{obFusc4ti0n_i5n't_EncRypt1oN}

Solved by: amkim13
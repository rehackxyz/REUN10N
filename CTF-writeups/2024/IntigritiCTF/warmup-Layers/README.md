# Layers

Solved by: @OS1R1S

## Question:
Weird way to encode your data, but OK! 🤷‍♂️

## Solution:
1. the number is just a trap. `ls -la` you will look the timestamp is not async with the number 0-55
2. make a script to extract the binary follow the timestamp not the file name (0-55)
3. Script:
```
import os

directory = "./Layer"

files = [(f, os.path.getmtime(os.path.join(directory, f))) for f in os.listdir(directory) if f.isdigit()]
files.sort(key=lambda x: x[1])  # Sort by timestamp

ascii_result = ""


for filename, _ in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r') as file:
        binary_data = file.read().strip()  # Read binary data
        ascii_result += chr(int(binary_data, 2))  # Convert binary to ASCII

print(ascii_result)
#SU5USUdSSVRJezdoM3IzNV9sNHkzcjVfNzBfN2gxNV9jaDRsbDNuNjN9
```
4. then the last one is base64 decode
5. `echo SU5USUdSSVRJezdoM3IzNV9sNHkzcjVfNzBfN2gxNV9jaDRsbDNuNjN9 | base64 -d`

**Flag:** `INTIGRITI{7h3r35_l4y3r5_70_7h15_ch4ll3n63}`

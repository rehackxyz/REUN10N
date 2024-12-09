# Antihash

Solved by: @OS1R1S

## Question:
Hash functions are really just turning strings into shorter, more jumbled strings, right? So I made an antihash function, it turns strings into longer, more jumbled strings! Can you guess what my input was?


## Solution:
```
sbox = [
    81, 50, -23, -66, -13, 100, -58, 79, 13, -47, 127, 111, 117, 128, -84, 10,
    123, -2, 28, 2, -102, 108, -63, 7, -22, 20, 96, -95, 66, 40, 52, -85,
    75, 53, 94, -72, -67, -1, -5, -71, -49, 6, 67, -92, 38, -64, -120, 55,
    102, -14, 116, -16, 16, -125, 124, 122, 74, -53, 86, 8, -36, -9, -27, 5,
    98, -119, 99, 87, 43, -94, 104, -56, -57, 47, -41, 32, 19, 109, -122, -91,
    12, -74, -6, 82, -20, 103, 35, 48, 85, -86, -79, -126, -108, -50, -100, -81,
    -35, 125, 26, -76, 92, -55, 29, -75, -123, -59, -101, -80, 54, -99, 114, 61,
    89, -112, -31, -12, 113, 22, -28, 84, -37, 33, -97, -114, 3, 58, 69, 70,
    -38, -106, -82, -44, 101, 120, 93, 62, -11, 77, -32, 115, 4, -65, 39, 112,
    -52, 90, 57, -113, 14, 9, 11, 80, -117, -69, -51, 83, -39, -115, 41, 88,
    64, 15, -7, -89, -121, 91, -10, 24, 45, -90, -104, 49, -19, 78, 72, -105,
    -60, 18, -77, -83, -4, -21, 106, -15, 31, 59, -46, -73, 44, -110, -87, -62,
    17, 34, -34, -88, 105, -109, 56, -8, -33, -68, -25,  65, -43, 60, 36, -96,
    -116, -127, -78, 126, -3, -98, -111, -124, 73, 42, 110, 1, 63, -26, 119, -48,
    -24, 46, -29, -61, 95, -54, -30, -45, -118, -107, 118, 30, -18, 71, -17, 25,
    107, -40, 121, 23, -70, 37, -93, 0, 68, 76, -42, 51, 27, -103, 97, 21
]

reverse_sbox = [0] * 256
for i in range(256):
    reverse_sbox[sbox[i] % 256] = i

def reverse_inflate(data, size):
    inflated = bytearray(size * 3 // 2)  # Adjusted size for inflation
    for i in range(size):
        inflated[i] = data[i]
        if i % 2 == 1:
            inflated[size + i // 2] = data[i] ^ 0x14
    return bytes(inflated[:size * 3 // 2])  # Return only the relevant portion

def reverse_shuffle(data, size):
    result = bytearray(size)
    for i in range(size):
        result[i] = data[size - i - 1]  # Reverse the order
    return bytes(result)

def reverse_substitute(data, size):
    return bytes([reverse_sbox[b % 256] for b in data[:size]])

def read_output_file():
    with open('output.txt', 'r') as f:
        content = f.read().strip().split()
        return bytes([int(x, 8) for x in content])  # Read as octal

def reverse_process():
    data = read_output_file()
    inflated_data = reverse_inflate(data, len(data))
    shuffled_data = reverse_shuffle(inflated_data, len(inflated_data))
    final_data = reverse_substitute(shuffled_data, len(shuffled_data))
    utf8_data = final_data.decode('utf-8', errors='replace')
    print(utf8_data[::-1])

reverse_process()
```
Then  manually decode

![3](https://i.ibb.co/LxNLv7v/rw.png)

**Flag:** `PP{4-cl4551c-1nS3Cu217y-bY-0b5cu217y}`

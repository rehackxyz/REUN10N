# Forensic - codebreaker
Solved by **warlocksmurf** and **0x251e**\
Original writeup by **warlocksmurf** - https://warlocksmurf.github.io/posts/wanictf2024/

## Question
I, the codebreaker, have broken the QR code!

## Solution
The corrupted QR code can be reconstructed by following the structure and format of a QR code. We increased the brightness/contrast as it helps in removing foreign drawings/pixels above the actual image.

Manual repair was done and the final image can be scanned.
![repaired-qr](https://i.ibb.co/t2V2RWT/Screenshot-2024-06-24-at-12-22-50-AM.png)

### Flag
`FLAG{How_scan-dalous}`

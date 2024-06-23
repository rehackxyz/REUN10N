# Forensic - tiny_10px
Solved by **warlocksmurf**\
Original writeup by **warlocksmurf** - https://warlocksmurf.github.io/posts/wanictf2024/

## Question
What a small world!

## Solution
We are given a small jpg image to investigate. Since we are given a jpg image, a common steganography method was hiding a flag by manipulating the image's dimensions. Here is a good [reference](https://cyberhacktics.com/hiding-information-by-changing-an-images-height/) I always use to understand jpg formats.

The flag was received after 'bruteforcing' width and height for quite some times.

### Flag
`FLAG{b1g_en0ugh}`

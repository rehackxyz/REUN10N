# Leaky Pipes
Solved by **zachwong_02**

Full writeup available at https://zach-wong.gitbook.io/easy-reads/osctf-2024-writeups/leaky-pipes-pwn
## Question
Welcome to Leaky Pipes, where a seemingly innocent program has sprung a serious leak! Your mission is to uncover the concealed flag hidden within the program. Will you be the one to patch the leak and reveal the hidden secret?

## Solution
1. type %x  200 times
2. go to cyberchef, swap endianess and decode from hex
3. start deleting "bad bytes" from the start

### Flag
`OSCTF{F0rm4t_5tr1ngs_l3ak4g3_l0l}`

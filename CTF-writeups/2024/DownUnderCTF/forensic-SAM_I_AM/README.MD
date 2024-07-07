# SAM I AM
Solved by **zachwong_02**\
**warlocksmurf** also created the full writeup here https://warlocksmurf.github.io/posts/ductf2024/#sam-i-am-forensics

## Question
The attacker managed to gain Domain Admin on our rebels Domain Controller! Looks like they managed to log on with an account using WMI and dumped some files. Can you reproduce how they got the Administrator’s Password with the artifacts provided?


## Solution
First
```
impacket-secretsdump -sam sam.bak -system system.bak local
```

Then crack it
```
john --wordlist=/usr/share/wordlists/rockyou.txt 4john
```

### Flag
`DUCTF{!checkerboard1}`

# Forensic - Surveillance_of_sus
Solved by **warlocksmurf**\
Original writeup by **warlocksmurf** - https://warlocksmurf.github.io/posts/wanictf2024/

## Question
I found an unknown file, and upon opening it, it caused some strange behavior, so I took a memory dump!\

How was the attack carried out?

Note: the file is too big, so it will not be uploaded here.

## Solution
We are given a cache file to investigate.

Using tools like `bmc-tools` and `RdpCacheStitcher`, the flag can be obtained.
```
└─$ python bmc-tools.py -s ~/Desktop/shared/WaniCTF/for-Surveillance-of-sus/Cache_chal.bin -d ~/Desktop/shared/WaniCTF/for-Surveillance-of-sus/
[+++] Processing a single file: '/home/kali/Desktop/shared/WaniCTF/for-Surveillance-of-sus/Cache_chal.bin'.
[===] 650 tiles successfully extracted in the end.
[===] Successfully exported 650 files.
```

### Flag
`FLAG{RDP_is_useful_yipeee}`

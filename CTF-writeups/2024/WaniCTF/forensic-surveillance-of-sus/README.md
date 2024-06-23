# Forensic - Surveillance_of_sus
Solved by **warlocksmurf**\
Original writeup by **warlocksmurf** - https://warlocksmurf.github.io/posts/wanictf2024/

## Question
A PC is showing suspicious activity, possibly controlled by a malicious individual.

It seems a cache file from this PC has been retrieved. Please investigate it!


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

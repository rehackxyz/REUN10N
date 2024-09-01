# bad packets

Solved by **yappare**

## Question
Our SOC says that there seems to be some curious activities within one of our servers. They provided a pcap file but I can't find what they're talking about.

## Solution
Analysing the pcap given, we observed few key points:
- `oldcss`
- `images?guid=`

Both of these hinted us this might be Trevor C2 payloads.

This was helped by reading the article by Nasreddine Bencherchali\
Reference: https://nasbench.medium.com/understanding-detecting-c2-frameworks-trevorc2-2a9ce6f1f425

Extracting all HTTP packets and using the TrevorC2 cyberchef recipe, https://github.com/1tchyBa11z/trevorc2-cyberchef we managed to find the flag.

Also we found another tool, which is much better. https://github.com/Abdelrahme/Trevorc2_decrypt/blob/main/trevorc2_decrypt.py

### Flag
`CSCTF{chang3_y0ur_variab13s_b3for3_d3pl0ying}`

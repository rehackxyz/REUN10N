# Baby First Forensics

Solved by **zachwong_02**\
**warlocksmurf** also created the full writeup here https://warlocksmurf.github.io/posts/ductf2024/#babys-first-forensics-forensics

## Question
They've been trying to breach our infrastructure all morning! They're trying to get more info on our covert kangaroos! We need your help, we've captured some traffic of them attacking us, can you tell us what tool they were using and its version?
NOTE: Wrap your answer in the DUCTF{}, e.g. DUCTF{nmap_7.25}

## Solution
```
strings capture.pcap | grep Agent
```

### Flag
`DUCTF{Nikto_2.1.6}`

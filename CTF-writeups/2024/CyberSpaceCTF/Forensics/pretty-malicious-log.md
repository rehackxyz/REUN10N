# Pretty Malicious Log

Solved by **0x251e**

## Question
I was trying to install the adobe crack and many weird things happened to my PC. Can you analyze the log and figure out what's going on?

## Solution
The file can be opened using Process Monitor. It was then analysed.

```
Question 1:
What program produced this log file?
Your answer: procmon
Correct!
```

```
Question 2:
How many registry keys got successfully modified by the malware?
Your answer: 13
Correct!
```
- Operation is RegSetValue
- PPID is 1184 (PID of adobe.exe)

```
Question 3:
What is the MITRE ID of the persistence technique used by the malware?
Your answer: T1547.001
Correct!
```
Question 3: \Run\mOkkYMEs.exe -> registry run keys

```
Question 4:
What is the name of the file that is added to autoruns by the malware?
Your answer: mOkkYMEs.exe
Correct!
```
Filter:
- Operation is ReSetValue
- Path contains \Run
- Result is SUCCESS

```
Question 5:
Which thread ID is responsible to create the environment for malware to run?
Your answer: 5352
Correct!
```
- Look at process tree, check its PPID
- Filter down path contains HKLM\SOFTWARE\Microsoft\WindowsRuntime
- Last for 0.0000015 

Reference: https://www.youtube.com/watch?v=8U2ivK8pts0


### Flag
`CSCTF{Pr0cm0n_1s_4_h3lpFul_sy5int3rn4l!_0x22defba1}`

# event-code-hunt

Solved by: @aan

## Question:
Maya Elmer managed to seize one of The Consortium’s computers, but when she tried to access a critical file, a sudden blue box flashed across her screen, and the file was instantly encrypted. Now, with the clock ticking, participants must step in to decrypt the file and uncover the hidden contents. The Consortium's encryption is tough to crack, and only the most determined will succeed in revealing the secrets locked away within.


## Solution:
1. In the PowershellOP event log file, there is a python script executed which is a simple xor cipher

`python3 .\Documents\Chrome.py .\Documents\flag.txt .\Documents\encrypt_flag.txt I_Like_Big_Bytes_And_I_cannot_Lie!``

2. further analyzation shows that the key is included in the event log

**Flag:** `NICC{Maya_Elmer_D3t3cts_Mal1c10us_P4yl04d_1n_3v3ntL0gs}`

Solved by: OS1R1S

### Question:
Do you dare to accept the Stego Gambit? I know you can find the checkmate but the flag!!

Challenge Image:
![[chall.png]]

### Solution:
1. The chess move was `Bh1Kxa2_Qg2#`, with that info can be use to crack it with steg
```bash
$ stegcracker chall.jpg sol.txt
StegCracker 2.1.0 - (https://github.com/Paradoxis/StegCracker)
---STRIP---

Counting lines in wordlist..
Attacking file 'chall.jpg' with wordlist 'sol.txt'..
Successfully cracked file with password: Bh1Kxa2_Qg2#
Tried 31 passwords
Your file has been written to: chall.jpg.out
Bh1Kxa2_Qg2#

$ cat chall.jpg.out
KashiCTF{573g0_g4m617_4cc3p73d}
```

**Flag:** `KashiCTF{573g0_g4m617_4cc3p73d}


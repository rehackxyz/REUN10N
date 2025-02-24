# Corruption

Solved by: OS1R1S
### Question:
A corrupt drive I see...

### Solution:
1. Use FTK to analyze artifacts
2. Export both file
3. Grep the flag 
```bash
$ strings * | grep "CTF"
KashiCTF{}
KashiCTF{FSCK_mE_B1T_by_b1t_Byt3_by_byT3}
```

**Flag:**`KashiCTF{FSCK_mE_B1T_by_b1t_Byt3_by_byT3}`
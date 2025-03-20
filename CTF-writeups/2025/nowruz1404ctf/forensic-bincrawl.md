# Bincrawl
Solved by: @benkyou

### Question:
The first step in dealing with a bin file?

### Solution:
- Binwalk challenge file
- Use `grep -r FMCTF _a.bin.extracted/ | cut -d':' -f2 | sort | uniq`

**Flag:** `FMCTF{8Inw4lK_3x7R4c7_L2m4_4U70m47ic4lLy!!}`


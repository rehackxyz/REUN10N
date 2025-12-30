Challenge name: BlackStar
Challenge Description: In the void between light and shadow, a star collapses upon itself, consuming its own brilliance, leaving only darkness. What secrets does it hide within?

FLAG: RE:CTF{b14CKS74R_F4LLs_7rUTh_r!S3S}

## Solution

1. open hex editor to replace the fifth byte of the ELF to 0x01 (ELF 32-bit e_ident[EI_CLASS])
2. use gdb to dump decrypted blob at address 0x804c044 and ROR-3 
break *0x080497e7
r
x/48bx 0x804c060
x/1dw 0x804c044
3. extract key from .blackstar section and decrypt with ROR47 and RC6 

Flag: RE:CTF{b14CKS74R_F4LLs_7rUTh_r!S3S}


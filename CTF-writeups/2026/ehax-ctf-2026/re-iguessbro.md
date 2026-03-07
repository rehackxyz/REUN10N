# re - i guess bro

Flag: `EH4X{y0u_gu3ss3d_th4t_r1sc_cr4ckm3}`

`main` reads input, strips newline, and enforces length = 0x23 (35).

The verifier rejects the two decoy strings:

`EH4X{n0t_th3_r34l_fl4g}`

`EH4X{try_h4rd3r_buddy}`

The actual check function builds a 35-byte buffer by decoding an encoded byte array from `.rodata` using:

`decoded[i] = encoded[i] XOR (7*i) XOR 0xA5` (xor uses the low 8 bits)

It then byte-compares the input against that decoded buffer.

Solved by: yappare
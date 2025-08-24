---
Base85-decode → reverse bytes → multiply each byte by 7⁻¹ mod 256 (i.e., 183) → XOR with the 7-byte key sha256("skibidiskibidi")[:7]. repeat

Flag: `brunner{tr4l4l3r0_b0mb4rd1r0_r3v3rs3_3ng1n33r1ng_sk1b1d1_m4st3r}`


Solved by: zeqzoq
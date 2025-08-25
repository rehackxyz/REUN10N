1. Found deleted file do_not_open_this.txt → string: C0u1d_Th1$_B3_f0r_z1p?
2.Carved Unalloc_8_5823488_1064934400.png from unallocated space.
3. Ran binwalk → detected hidden 7-zip archive at offset 0x295000.
Extracted archive:
`dd if=Unalloc_8_5823488_1064934400.png of=recovered.7z bs=1 skip=2707456 count=2500593`
4. Archive was password-protected → used hint string as password.
5. Opened successfully → got flag:

Flag `brunner{cu$t4rd_1z_k1ng}`

Solved by: 1337_flagzz
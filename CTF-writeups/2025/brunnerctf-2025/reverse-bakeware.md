1. Initial Binary Analysis

Program looks for Grandmas_Secret_Baking_Family_Recipe.txt
Computes SHA-256 hash and compares against hardcoded value: 502ff05a7b51b76e740b19cc4957ad118897a25becbb87fcb662a14b2e56a5d9
If hash doesn't match, exits with "File not found. Nothing to steal :("

2. Bypass Hash Check

Set breakpoint at hash comparison (0x408d84)
Use debugger to force the conditional jump to succeed:
bashb *0x408d84
set $eflags |= 0x40  # Set Zero Flag
c


3. Key Extraction Analysis

After bypass, program calls get_key_part() function 8 times
Each call extracts bytes from two hardcoded strings containing various text
Function uses from_iter to process the strings and extract specific characters

4. Extract the Final Key

Set breakpoint after all get_key_part calls complete
Key gets concatenated and verified to be exactly 32 bytes
Extracted Key: OTHellOTotallyStealGoodRecipes!!

5. Find the IV

Analyzed hardcoded strings in get_key_part function
Found hex string: 12345678901234560123456789abcdef
IV: 12345678901234560123456789abcdef (converted from hex)

6. Decrypt the Flag

Algorithm: AES-256-CBC
Key: OTHellOTotallyStealGoodRecipes!! (32 bytes)
IV: 12345678901234560123456789abcdef (16 bytes)
Used Python cryptography library to decrypt the .enc file
Handled PKCS7 padding removal
Result: Successfully decrypted flag content

<later upload python decryption script>

Flag:`brunner{Gr4ndm4_sh0u1d_R34lL7_l34rn_b3tt3r_0ps3c}`

Solved by: 1337_flagzz
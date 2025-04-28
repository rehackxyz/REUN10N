# Solution
Bypassed the filter using a case variation trick:

- Using uppercase for part of the domain: `\x06TikTok\x03Com\x00` instead of `\x06tiktok\x03com\x00`
- Sending this query to the server (`0000001c1234010000010000000000000654696b546f6b03436f6d0000100001`)
- DNS servers treat domain names case-insensitively, so "TikTok.Com" resolves to the same record as "tiktok.com". However, the byte-level filter looking for `tiktok\x03com` doesn't match our uppercase version, allowing our query to bypass the filter.

Flag: `UMDCTF{W31C0M3_84CK_4ND_7H4NK5_F0r_Y0Ur_P4713NC3_4ND_5UPP0r7_45_4_r35U17_0F_Pr351D3N7_7rUMP_71K70K_15_84CK_1N_7H3_U5}`


Solved by: w_11_xuan

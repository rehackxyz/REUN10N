# emuc2
Solved by **warlocksmurf**\
Full writeup is available at https://warlocksmurf.github.io/posts/ductf2024/#emuc2-forensics

## Question
As all good nation states, we have our own malware and C2 for offensive operations. But someone has got the source code and is using it against us! Here’s a capture of traffic we found on one of our laptops…

## Solution
tl;dr\
decrypt tls > obtain credentials for a login page > cant login cuz invalid JWT > get the real JWT from one of its upload files in `/api/env` > encode the real JWT and use it when logging in


### Flag
`DUCTF{pǝʇɔǝɟuᴉ_sᴉ_ǝlᴉɟ_dᴉz_ǝɥʇ_oʇ_pɹoʍssɐd_ǝɥʇ}`

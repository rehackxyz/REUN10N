Perl Ransomware

1. Ransomware can be recovered from `/var/log/lighttpd/access.log`
2. Get all the Base64 values from the URL parameter and decode them
3. Files are encrypted with AES-256 CBC Mode
4. AES Key is `L0s3@llYourF1l3s` based on the command from the URL parameter
5. IV is provided in the ransomware as `R4ND0MivR4ND0Miv`
6. Flag is in `/files/kitten08.jpg.enc`

flag: `flag{b5f18f25dd58d68d083e03260c3b6f34}`

Solved by: zachwong_02
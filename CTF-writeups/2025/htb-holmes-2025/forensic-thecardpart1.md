 The Cards
Q1 : Analyze the provided logs and identify what is the first User-Agent used by the attacker against Nicole Vale's honeypot. (string)
-> Lilnunc/4A4D - SpecterEye
-> Found this in the access.log since it is the only username and pass have the protocol of "200" which means that the attempt is successful.

Q2 : It appears the threat actor deployed a web shell after bypassing the WAF. What is the file name? (filename.ext)
-> temp_4A4D.php
-> Based on application.log :
2025-05-18 15:02:12 [CRITICAL] webapp.security - Web shell access detected - temp_4A4D.php executed by 121.36.37.224

Q3 : The threat actor also managed to exfiltrate some data. What is the name of the database that was exfiltrated? (filename.ext)
-> database_dump_4A4D.sql
-> Based on application.log :
2025-05-18 14:58:23 121.36.37.224 - - [18/May/2025:15:58:23 +0000] "GET /uploads/database_dump_4A4D.sql HTTP/1.1" 200 52428800 "-" "4A4D RetrieveR/1.0.0"

Q4 : During the attack, a seemingly meaningless string seems to be recurring. Which one is it? (string)
-> 4A4D
Self explanatory

Q5 : OmniYard-3 (formerly Scotland Yard) has granted you access to its CTI platform. Browse to the first IP:port address and count how many campaigns appear to be linked to the honeypot attack.
-> 5


Q6 : How many tools and malware in total are linked to the previously identified campaigns? (number)
-> 9 

Solved by: 1337_flagzz
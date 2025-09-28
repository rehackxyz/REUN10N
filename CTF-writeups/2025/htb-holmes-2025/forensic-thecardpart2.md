Q7 : It appears that the threat actor has always used the same malware in their campaigns. What is its SHA-256 hash? (sha-256 hash)
http://83.136.250.223:43439/ (CogWork-Intel Graph)
-> 7477c4f5e6d7c8b9a0f1e2d3c4b5a6f7e8d9c0b1a2f3e4d5c6b7a8f9e0d17477

Q8 : Browse to the second IP:port address and use the CogWork Security Platform to look for the hash and locate the IP address to which the malware connects. (Credentials: nvale/CogworkBurning!)
http://83.136.250.223:59336/ (CogWork Security)
-> copy paste the hash earlier

Q9 : What is the full path of the file that the malware created to ensure its persistence on systems? (/path/filename.ext) \\Using same site
-> /opt/lilnunc/implant/4a4d_persistence.sh 

Q10 : Finally, browse to the third IP:port address and use the CogNet Scanner Platform to discover additional details about the TA's infrastructure. How many open ports does the server have?
http://83.136.250.223:48105/ (CogNet Scanner)
-> Investigate using the IP we got from cogwork security (74.77.74.77)
-> Under the details risk management got the number of the open port

Q11 : Which organization does the previously identified IP belong to? (string)
-> SenseShield MSP (can see the img)

Q12 : One of the exposed services displays a banner containing a cryptic message. What is it? (string)
-> He's a ghost I carry, not to haunt me, but to hold me together - NULLINC REVENGE (in the services tab)

Solved by: 1337_flagzz
1. What is the Linux kernel version of the provided image? (string)
5.10.0-35-amd64

2. The attacker connected over SSH and executed initial reconnaissance commands. What is the PID of the shell they used? (number)
13608

3. After the initial information gathering, the attacker authenticated as a different user to escalate privileges. Identify and submit that user's credentials. (user:password)
jm:WATSON0

4. The attacker downloaded and executed code from Pastebin to install a rootkit. What is the full path of the malicious file? (/path/filename.ext)
/usr/lib/modules/5.10.0-35-amd64/kernel/lib/Nullincrevenge.ko

5. What is the email account of the alleged author of the malicious file? (user@example.com)
i-am-the@network.now

6. The next step in the attack involved issuing commands to modify the network settings and installing a new package. What is the name and PID of the package? (package name,PID)
dnsmasq,38687

7. Clearly, the attacker's goal is to impersonate the entire network. One workstation was already tricked and got its new malicious network configuration. What is the workstation's hostname?
Parallax-5-WS-3

8. After receiving the new malicious network configuration, the user accessed the City of CogWork-1 internal portal from this workstation. What is their username? (string)
mike.sullivan


9. Finally, the user updated a software to the latest version, as suggested on the internal portal, and fell victim to a supply chain attack. From which Web endpoint was the update downloaded?
/win10/update/CogSoftware/AetherDesk-v74-77.exe

10. To perform this attack, the attacker redirected the original update domain to a malicious one. Identify the original domain and the final redirect IP address and port. (domain,IP:port)
updates.cogwork1.net,13.62.49.86:7477

Solved by: 1337_flagzz
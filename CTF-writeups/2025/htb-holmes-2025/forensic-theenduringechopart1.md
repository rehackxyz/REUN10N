1. What was the first (non cd) command executed by the attacker on the host? (string)
systeminfo 

2. Which parent process (full path) spawned the attacker’s commands? (C:\FOLDER\PATH\FILE.ext)
C:\Windows\System32\wbem\WmiPrvSE.exe

3. Which remote-execution tool was most likely used for the attack? (filename.ext)
WmiExec.py

4. What was the attacker’s IP address? (IPv4 address)
10.129.242.110

5. What is the first element in the attacker's sequence of persistence mechanisms? (string)
SysHelper Update

6.dentify the script executed by the persistence mechanism. (C:\FOLDER\PATH\FILE.ext)
C:\Users\Werni\AppData\Local\JM.ps1

7. What local account did the attacker create? (string)
svc_netupd

8. What domain name did the attacker use for credential exfiltration? (domain)
NapoleonsBlackPearl.htb

9. What password did the attacker's script generate for the newly created user? (string)
Watson_20250824160509

10. What was the IP address of the internal system the attacker pivoted to? (IPv4 address)
192.168.1.101

11. Which TCP port on the victim was forwarded to enable the pivot? (port 0-65565)
9999

Solved by: 1337_flagzz
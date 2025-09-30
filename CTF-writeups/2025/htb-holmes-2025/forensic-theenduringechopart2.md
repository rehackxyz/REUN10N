12. What is the full registry path that stores persistent IPv4→IPv4 TCP listener-to-target mappings? (HKLM......)
HKLM\SYSTEM\CurrentControlSet\Services\PortProxy\v4tov4\tcp

13. What is the MITRE ATT&CK ID associated with the previous technique used by the attacker to pivot to the internal system? (Txxxx.xxx)
T1090.001

14. Before the attack, the administrator configured Windows to capture command line details in the event logs. What command did they run to achieve this? (command)
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\Audit" /v ProcessCreationIncludeCmdLine_Enabled /t REG_DWORD /d 1 /f 

Solved by: 1337_flagzz
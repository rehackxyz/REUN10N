# dfir - Stockpile Breach

Flag: `0xL4ugh{1t_w4s_just_@_warmup_579ae58e75}`

Solved by OS1RI1S

It seems like Khaled, an employee in the finance department, was looking for an easy way to monitor stock market trends. He downloaded an application that claimed to provide real-time stock updates. However, security logs indicate that this app may not have been what it claimed.
(1/11) What is the domain of the application that Khaled


```
└─$ strings "./Users/khaled.allam/AppData/Local/Microsoft/Edge/User Data/Default/History" | grep "monitorStock.exe"
=C4ec5be78-89d9-4375-a5a2-1ca7ab45378aC:\Users\khaled.allam\Downloads\monitorStock.exeC:\Users\khaled.allam\Downloads\monitorStock.exe
http://app.finance.com/monitorStock.exe
```

answer: app.finance.com


---


(2/11) At what exact timestamp was the malicious app downloaded? (YYYY-MM-DD HH:MM:SS UTC)

From history

```
"2","4ec5be78-89d9-4375-a5a2-1ca7ab45378a","C:\Users\khaled.allam\Downloads\monitorStock.exe","C:\Users\khaled.allam\Downloads\monitorStock.exe","13383376626598500","15865856","15865856","1","6","0","","13383376646518096","1","13383376883979292","0","http://app.finance.com/","","
```

```
from datetime import datetime, timedelta
chrome_base = datetime(1601, 1, 1)
start_time = 13383376626598500
download_utc = chrome_base + timedelta(microseconds=start_time)
print(download_utc.strftime('%Y-%m-%d %H:%M:%S'))
#2025-02-07 04:37:06
```

Answer: 2025-02-07 04:37:06 UTC


---

(3/11) When did Khaled execute the downloaded application? (YYYY-MM-DD HH:MM:SS UTC)

```
C\Windows\prefetch\MONITORSTOCK.EXE-4D4C5193.pf

using PECMD:
Command line: PECmd.exe -f MONITORSTOCK.EXE-4D4C5193.pf

Created on: 2026-01-23 15:39:28
Modified on: 2025-02-07 04:41:34
Last accessed on: 2026-01-23 16:45:57

Executable name: MONITORSTOCK.EXE
Hash: 4D4C5193
File size (bytes): 30,058
Version: Windows 10 or Windows 11

Run count: 1
Last run: 2025-02-07 04:41:24
```

answer: 2025-02-07 04:41:24 UTC

---

What is the SHA256 hash of the malicious application?

```
using Hayabusa:
Commandline: hayabusa-3.7.0-win-x64.exe csv-timeline -d .\logs\ -o hehe.csv


"2025-02-07 12:54:56.159 +08:00","Proc Exec","info","EZ-CERT","Sysmon",1,552,"Cmdline: ""C:\Windows\Temp\monitorStock.exe"" ¦ Proc: C:\Windows\Temp\monitorStock.exe ¦ User: EZ-CERT\khaled.allam ¦ ParentCmdline: C:\Windows\Explorer.EXE ¦ LID: 0x1ad79 ¦ LGUID: A9F18D2D-920C-67A5-79AD-010000000000 ¦ PID: 4472 ¦ PGUID: A9F18D2D-9220-67A5-4A00-000000000100 ¦ ParentPID: 3344 ¦ ParentPGUID: A9F18D2D-920F-67A5-3900-000000000100 ¦ Description: - ¦ Product: - ¦ Company: - ¦ Hashes: MD5=A95672C643FB8521FAB9B7CAE1366F7E,SHA256=314AA91A2AD7770F67BF43897996A54042E35B6373AE5D6FEB81E03A077255A7,IMPHASH=F0EA7B7844BBC5BFA9BB32EFDCEA957C","CurrentDirectory: C:\Windows\system32\ ¦ IntegrityLevel: Medium ¦ ParentImage: C:\Windows\explorer.exe ¦ TerminalSessionId: 1 ¦ UtcTime: 2025-02-07 04:54:56.114","85790e3e-e270-499f-a6ad-f8afe85c35f1"

```

answer: 314AA91A2AD7770F67BF43897996A54042E35B6373AE5D6FEB81E03A077255A7

---

What is the IP and port of the C2 server that the app connected to?

```
"2025-02-07 12:54:57.584 +08:00","Net Conn","info","EZ-CERT","Sysmon",3,553,"Initiated: true ¦ Proto: tcp ¦ SrcIP: 192.168.45.128 ¦ SrcPort: 49701 ¦ SrcHost: EZ-CERT.localdomain ¦ TgtIP: 3.121.219.28 ¦ TgtPort: 8888 ¦ TgtHost: app.finance.com ¦ User: EZ-CERT\khaled.allam ¦ Proc: C:\Windows\Temp\monitorStock.exe ¦ PID: 4472 ¦ PGUID: A9F18D2D-9220-67A5-4A00-000000000100","DestinationIsIpv6: false ¦ DestinationPortName: - ¦ RuleName: - ¦ SourceIsIpv6: false ¦ SourcePortName: - ¦ UtcTime: 2025-02-07 04:54:56.305","a87defd7-1f87-4a34-8864-415ccb2ef21c"
```

answer: 3.121.219.28:8888

4472
10200


---

What was the first command the attacker used to ensure his access?

```
"2025-02-07 12:41:24.068 +08:00","Proc Exec","info","EZ-CERT","Sysmon",1,164,"Cmdline: ""C:\Users\khaled.allam\Downloads\monitorStock.exe""
"2025-02-07 12:41:40.529 +08:00","Proc Exec","info","EZ-CERT","Sysmon",1,168,"Cmdline: ""C:\Windows\system32\whoami.exe""
```

answer: whoami

---

Question 7: What is the registry key the attacker added for persistence?

```
""C:\Windows\system32\reg.exe"" add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v FilePersistence /t REG_SZ /d C:\Windows\Temp\monitorStock.exe /f
```

answer: Software\Microsoft\Windows\CurrentVersion\Run

---

Question 8: What was the value of the persistence registry key?

```
""C:\Windows\system32\reg.exe"" add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v FilePersistence /t REG_SZ /d C:\Windows\Temp\monitorStock.exe /f
```

answer: C:\Windows\Temp\monitorStock.exe

---

Question 9: When was the file copied to the new directory (The directory in the previous question)? (Format: YYYY-MM-SS HH:MM:SS)

```
Convert to UTC
"2025-02-07 12:43:51.962 +08:00","File Created (Sysmon Alert)","med","EZ-CERT","Sysmon",11,177,"Rule: EXE ¦ Path: C:\Windows\Temp\monitorStock.exe ¦ Proc: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe ¦ PID: 4240 ¦ PGUID: A9F18D2D-8EFF-67A5-7603-000000000100","CreationUtcTime: 2025-02-07 04:43:51.961 ¦ User: EZ-CERT\khaled.allam ¦ UtcTime: 2025-02-07 04:43:51.961","c5e6b545-73a4-4650-ae97-67c239005382"
```

answer: 2025-02-07 04:43:51 UTC

---

Question 10: When was the persistence registry key added? (Format: YYYY-MM-SS HH:MM:SS)

```
Convert to UTC
"2025-02-07 12:45:03.321 +08:00","Proc Exec","info","EZ-CERT","Sysmon",1,178,"Cmdline: ""C:\Windows\system32\reg.exe"" add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v FilePersistence /t REG_SZ /d C:\Windows\Temp\monitorStock.exe /f
```

answer: 2025-02-07 04:45:03 UTC

---


Question 11: Identify the framework used by the malicious file for command and control communication.
```
Hacktool of Sliver was uses
"2025-02-07 12:41:35.491 +08:00","HackTool - Sliver C2 Implant Activity Pattern","crit","EZ-CERT","Sysmon",1,166,"Cmdline: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -NoExit -Command [Console]::OutputEncoding=[Text.UTF8Encoding]::UTF8
```
answer: sliver

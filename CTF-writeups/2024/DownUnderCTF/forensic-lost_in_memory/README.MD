# Title
Solved by **by warlocksmurf & zachwong_02**\
Full writeup is available at https://warlocksmurf.github.io/posts/ductf2024/#lost-in-memory-forensics

## Question
Looks like one of our Emu soldiers ran something on an Outpost machine and now it&#39;s doing strange things. We took a memory dump as a precaution. Can you tell us whats going on? This challenge has four parts to combine into the final flag with _ between each answer. Find all four answers and combine them into the flag as all lower case like DUCTF{answer1_answer2_answer3_answer4} eg. DUCTF{malicious.xlsm_invoke- mimikatz_malware.exe-malware2.exe_strong-password123}

1. What was the name of the malicious executable? eg malicious.xlsm
2. What was the name of the powershell module used? eg invoke-mimikatz
3. What were the names of the two files executed from the malicious executable (In
alphabetical order with - in between and no spaces)? eg malware.exe-malware2.exe
4. What was the password of the new account created through powershell? eg strong-
password123

## Solution

1. Investigate the memory dump given. Analysed the process tree and observed the notepad which stands the most. Two suspicious files were executed by the Notepad.exe (`monkey.doc.ps1`)
2 & 3. The content of `monkey.doc.ps1` was investigated and observed two DLL file were executed `kiwi.dll` and `emu.dll` using the PowerShell module (`Invoke-ReflectivePEInjection`)
4. Deobfuscation the script revealed the password (`5up3r-5ecur3`)

### Flag
`DUCTF{monkey.doc.ps1_invoke-reflectivepeinjection_emu.dll-kiwi.dll_5up3r-5ecur3}`

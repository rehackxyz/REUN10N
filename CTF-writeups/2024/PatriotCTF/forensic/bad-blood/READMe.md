# Bad Blood

Solved by: @ZeqZoq and @Cookies to SELL

- Category: forensic
- Description: 

Nothing is more dangerous than a bad guy that used to be a good guy. Something's going on... please talk with our incident response team.

Use `nc chal.competitivecyber.club 10001` to answer the questions in order to retrieve flag.

- Challenge File: suspicious.evtx

### Solutions:

##### Q1. Forensics found post exploitation activity present on system, network and security event logs. What post-exploitation script did the attacker run to conduct this activity?

Answer: Invoke-P0wnedshell.ps1

##### Q2. Forensics could not find any malicious processes on the system. However, network traffic indicates a callback was still made from his system to a device outside the network. We believe jack used process injection to facilitate this. What script helped him accomplish this?

Answer: Invoke-UrbanBishop.ps1

##### Q3. We believe Jack attempted to establish multiple methods of persistence. What windows protocol did Jack attempt to abuse to create persistence?

Answer: WinRM

##### Q4. Network evidence suggest Jack established connection to a C2 server. What C2 framework is jack using?

Answer: Covenant

**Flag:** `pctf{3v3nt_l0gs_reve4l_al1_a981eb}`


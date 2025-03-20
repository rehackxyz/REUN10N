# Samuel Dummper
Solved by: @yappare

### Question:
You know samuel?

### Solution:
- the files given are dumped sam files from windows
- use impacket to analyse `secretsdump.py -system SYSTEM -sam SAM local`
- crack the NTLM hashes `hashcat -m 1000 -a 0 hashes.txt wordlist.txt`
- `4c1f8668b38d6d34a96d442e9f9f8061:babigurl1`

**Flag:** `FMCTF{babigurl1}`


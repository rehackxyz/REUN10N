# encryptor
Solved by **whymir**

## Question
My friend sent me this app with an encoded flag, but he forgot to implement the decryption algorithm! Can you help me out?

## Solution

Decompile the APK give and look for `enc.txt` file. Search for the key

```
enc.txt - OIkZTMehxXAvICdQSusoDP6Hn56nDiwfGxt7w/Oia4oxWJE3NVByYnOMbqTuhXKcgg50DmVpudg=

Blowfish key- base64(ZW5jcnlwdG9yZW5jcnlwdG9y)
```


### Flag
`CSCTF{3ncrypt0r_15nt_s4Fe_w1th_4n_h4Rdc0d3D_k3y!}`

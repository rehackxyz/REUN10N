## Solution:
read `survival.gmi` and everything will be there including the password and new host
```py
from pwn import *
context.log_level = 'debug'

host, port = "chal.2025.ductf.net", 30063
io = remote(host, port, ssl=False)
    
password = "But%2Bripples%2Bshow%3Dtruth%25in%20motion"
io.send(f"gemini://{host}/password_protected.gmi?{password}\r\n".encode())

data = io.recvall(timeout=5).decode()
io.close()

print(data)
```

Flag:  `DUCTF{Cr1pPl3_Th3_1nFr4sTrUCtu53}`

Solved by: vicevirus
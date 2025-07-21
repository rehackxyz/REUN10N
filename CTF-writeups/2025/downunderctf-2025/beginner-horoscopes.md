## Solution:
interesting chall, gemini protocol
```py
from pwn import *

context.log_level = 'debug'
host, port = "chal.2025.ductf.net", 30015
io = remote(host, port, ssl=True, sni=host)

io.send(f"gemini://{host}/\r\n".encode())

page = io.recvall(timeout=5).decode()
print(page)
```

Flag:  `DUCTF{g3mini_pr0t0col_s4ved_us}`

Solved by: vicevirus
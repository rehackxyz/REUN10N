## Solution:
visit `/pages/rabid_bean_potato.gmi`
```py
from pwn import *

context.log_level = 'debug'
host, port = "chal.2025.ductf.net", 30015

io = remote(host, port, ssl=True, sni=host)
io.send(f"gemini://{host}/pages/rabid_bean_potato.gmi\r\n".encode())
page = io.recvall(timeout=5).decode(errors='ignore')

print(page)
```

Flag:  `DUCTF{rabbit_is_rabbit_bean_is_bean_potato_is_potato_banana_is_banana_carrot_is_carrot}`

Solved by: vicevirus
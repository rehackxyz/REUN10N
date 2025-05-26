### Sol  

Instead of using UUUU marker, we use DEFG

```
import sys
import base64

fname = r"C:\Users\zeqzoq\Downloads\nahamcon\gangster.zip"

data = open(fname, "rb").read()

marker = b"DEFG"
idx = data.find(marker)

start = idx + len(marker)
end   = data.find(b"\n", start)
b64   = data[start:end]

flag = base64.b64decode(b64).decode("ascii").strip()
print(flag)
```  

Flag:`flag{af1150f07f900872e162e230d0ef8f94}`

Solved by: zeqzoq
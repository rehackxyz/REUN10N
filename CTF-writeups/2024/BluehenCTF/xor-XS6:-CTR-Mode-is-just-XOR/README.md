# XS6: CTR Mode is just XOR

Solved by: @vicevirus

## Question:
`https://gist.github.com/AndyNovo/23d509307fc55fcebae1fd522ed04295`

## Solution:
```
import requests
from Crypto.Util.Padding import unpad

API_URL = "https://i8fgyps3o2.execute-api.us-east-1.amazonaws.com/default/ctrmode"

initial_pt = "00"
response = requests.get(API_URL, params={'pt': initial_pt})
data = response.json()

probiv = bytes.fromhex(data['probiv'])
flagenc = bytes.fromhex(data['flagenc'])

block_size = 16
decrypted_flag = b""

for block_num in range((len(flagenc) + block_size - 1) // block_size):
   
    counter = block_num.to_bytes(block_size - len(probiv), byteorder='big')
    pt_block = probiv + counter

    enc_response = requests.get(API_URL, params={'pt': pt_block.hex()}).json()
    key_stream = bytes.fromhex(enc_response['ciphertext'])[:block_size]

    flag_block = flagenc[block_num*block_size : (block_num+1)*block_size]
    decrypted_flag += bytes(x ^ y for x, y in zip(flag_block.ljust(block_size, b'\x00'), key_stream))

flag = unpad(decrypted_flag, block_size).decode()
print(flag) # import requests
from Crypto.Util.Padding import unpad

API_URL = "https://i8fgyps3o2.execute-api.us-east-1.amazonaws.com/default/ctrmode"

initial_pt = "00"
response = requests.get(API_URL, params={'pt': initial_pt})
data = response.json()

probiv = bytes.fromhex(data['probiv'])
flagenc = bytes.fromhex(data['flagenc'])

block_size = 16
decrypted_flag = b""

for block_num in range((len(flagenc) + block_size - 1) // block_size):
   
    counter = block_num.to_bytes(block_size - len(probiv), byteorder='big')
    pt_block = probiv + counter

    enc_response = requests.get(API_URL, params={'pt': pt_block.hex()}).json()
    key_stream = bytes.fromhex(enc_response['ciphertext'])[:block_size]

    flag_block = flagenc[block_num*block_size : (block_num+1)*block_size]
    decrypted_flag += bytes(x ^ y for x, y in zip(flag_block.ljust(block_size, b'\x00'), key_stream))

flag = unpad(decrypted_flag, block_size).decode()
print(flag)
```

**Flag:`UDCTF{th3r3_15_n0_sp00n_y0uv3_alr34dy_d3c1d3d_NE0}`** 

# XS8: XOR without XOR

Solved by: @vicevirus

## Question:
`https://gist.github.com/AndyNovo/84580af56a6294ed2576366018dc557c`

## Solution:

```
import requests

URL = "https://vbbfgwcc6dnuzlawkslmxvlni40zkayu.lambda-url.us-east-1.on.aws/"

def xor_iv(iv, original, desired, start=9):
    return bytes(iv[i] ^ original[i - start] ^ desired[i - start] if start <= i < start + len(original) else iv[i] for i in range(len(iv)))

def main():
    data = requests.get(URL).json()
    iv = xor_iv(bytes.fromhex(data['iv']), b"guest", b"admin")
    response = requests.get(URL, params={'token': data['token'], 'iv': iv.hex()}).json()
    print("Flag:" if "flag" in response else "Response:", response)

main()
```
**Flag:`udctf{1v_m4n1pul4t10n_FTW_just_anoth3r_x0R_4pplic4tion}`** 

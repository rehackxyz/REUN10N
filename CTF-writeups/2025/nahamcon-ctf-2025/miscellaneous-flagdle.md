### Sol  

``` 
#!/usr/bin/env python3
import requests

URL     = "http://challenge.nahamcon.com:30702/guess"
HEADERS = {"Content-Type": "application/json"}
HEX_CHARS = "0123456789abcdef"
L = 32
FILL = "z"

def guess(inner: str) -> str:
    payload = {"guess": f"flag{{{inner}}}"}
    r = requests.post(URL, json=payload, headers=HEADERS)
    r.raise_for_status()
    return r.json()["result"]

def main():
    known = ["?"] * L

    for i in range(L):
        for c in HEX_CHARS:
            trial = "".join(k if k != "?" else (c if idx==i else FILL)
                            for idx, k in enumerate(known))
            res = guess(trial)
            if res[i] == "🟩":
                known[i] = c
                print(f"Position {i:2d} = {c}")
                break

    flag = "flag{" + "".join(known) + "}"
    print("\nNi ha:", flag)

if __name__ == "__main__":
    main()
```

Flag:`flag{bec42475a614b9c9ba80d0eb7ed258c5}`

Solved by: zeqzoq
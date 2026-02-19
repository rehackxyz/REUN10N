# forensic - Tesla

```python
#!/usr/bin/env python3
import re

PATH = "Tesla.sub"

def expand_batch(line: str, varname: str, value: str) -> str:
    out = ""
    i = 0
    while i < len(line):
        if line[i] != "%":
            out += line[i]
            i += 1
            continue

        j = line.find("%", i + 1)
        if j == -1:
            out += line[i:]
            break

        token = line[i+1:j]

        # "%%" -> literal percent (not really needed here, but safe)
        if token == "":
            out += "%"
        else:
            m = re.fullmatch(re.escape(varname) + r":~(-?\d+),(\d+)", token)
            if m:
                start = int(m.group(1))
                ln = int(m.group(2))
                if start < 0:
                    start = len(value) + start
                out += value[start:start+ln]
            else:
                # any other %SOMETHING% in the obfuscation is junk -> empty
                out += ""

        i = j + 1
    return out

def main():
    raw = open(PATH, "rb").read().decode("utf-8", errors="replace")

    # 1) Extract 8-bit binary groups and turn into bytes
    bins = re.findall(r"\b[01]{8}\b", raw)
    blob = bytes(int(b, 2) for b in bins)

    # 2) Interpret as batch text (latin1 preserves bytes 1:1)
    s = blob.decode("latin1", errors="replace")
    lines = s.splitlines()

    # 3) Grab `set "VAR=VALUE"`
    m = re.search(r'set\s+"([^=]+)=(.*)"\s*$', lines[0])
    if not m:
        raise SystemExit("Could not find set \"VAR=VALUE\" in first line")
    varname, value = m.group(1), m.group(2)

    # 4) Expand all lines
    expanded = [expand_batch(l, varname, value) for l in lines]

    # 5) Pull the XOR key from the PowerShell string
    #    ... GetBytes('i could be something to this')
    key_m = re.search(r"GetBytes\('([^']+)'\)", "\n".join(expanded))
    if not key_m:
        raise SystemExit("Could not find key phrase in expanded PowerShell line")
    key = key_m.group(1).encode()

    # 6) Pull the hex ciphertext from comment line ":: <hex> ::"
    hex_m = re.search(r"::\s*([0-9a-fA-F]{20,})\s*::", "\n".join(expanded))
    if not hex_m:
        raise SystemExit("Could not find hex ciphertext in expanded comments")
    ct = bytes.fromhex(hex_m.group(1))

    # 7) XOR decrypt
    pt = bytes(ct[i] ^ key[i % len(key)] for i in range(len(ct)))
    print(pt.decode("utf-8", errors="replace").strip())

if __name__ == "__main__":
    main()
```
FLAG:`0xfun{d30bfU5c473_x0r3d_w1th_k3y}`

Solved by: ha1qal
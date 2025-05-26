# Solution

strings the flag.sh, it show the file uses bash, perl, openssl, base64  
`perl -pe 's/[^[:print:]]//g' flag.sh` shows the file content  
decode base64 in the file content but with openssl using `echo "" | | openssl base64 -A -d` and we will see full script  
the challenge mention to use hello as the crypt id but need to find the UID thats compatible with the openssl decrypt payload  
some scripting we got UID=1338  
then simulate the first stage of the payload to get the password
```
#!/usr/bin/env bash
set -euo pipefail

CRYPT_ID="hello"
THE_UID=1338

P_B64="llLvO8+J6gmLlp964bcJG3I3mY27I9ACsJTvXYCZv2Q="

P=$(printf '%s' "$P_B64" \
    | openssl enc -d -aes-256-cbc \
        -md sha256 -nosalt \
        -pass "pass:${CRYPT_ID}-${THE_UID}" \
        -a -A)

echo "→ Intermediate password (P) = $P"
```
so we get `QHh4K9JfgoACd2f4`

then just run with the flag.sh, specifying the crypt ID

```
$ PASSWORD=QHh4K9JfgoACd2f4 ./flag.sh hello
flag{f2ea4caf879bde891f0174f528c20682}
Congraulations!
```

Flag:`flag{f2ea4caf879bde891f0174f528c20682}`

Solved by: zeqzoq

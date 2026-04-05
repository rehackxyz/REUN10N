# web - Patisserie

**Vulnerability Identification**
The challenge contains a Cookie Parsing Discrepancy between the Python Flask proxy and the Node.js Express backend.

**Proxy (Python)**: Uses http.cookies.SimpleCookie to parse incoming cookies. It blocks the request if any parsed cookie name contains the substring "admin". SimpleCookie respects double quotes; it treats semicolons inside a quoted string as part of the cookie value, not as a delimiter.
+1

**Backend (Node.js)**: Uses cookie-parser. The underlying Node.js cookie module blindly splits the raw Cookie header by semicolons (;) and completely ignores double quotes during the splitting phase. The backend grants access to the flag if req.cookies.is_admin === "1".
```
curl -s -H 'Cookie: dummy="a; is_admin=1; b="' http://35.194.108.145:31604/admin | grep -oP 'tkbctf\{.*?\}'```

`tkbctf{qu0t3d_c00k13_smuggl1ng_p4rs3r_d1ff_7d3f8a2b}`

Compiled by: yappare
Solved by: g10d
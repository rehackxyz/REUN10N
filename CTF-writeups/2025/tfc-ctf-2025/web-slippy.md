There is a zipslip vulnerability so you can use symlinks to read files on the server. However, the directory that the flag is stored in is random, so we need a way to leak this.

We can get directory listing with `/debug/files?session_id`
```js
router.get('/debug/files', developmentOnly, (req, res) => {
    const userDir = path.join(__dirname, '../uploads', req.query.session_id);
```

The developmentOnly middleware does these checks. First, we need to leak the session store (`/app/server.js`) and secret key(`/app/.env`) using the zipslip. Then, because of `app.set('trust proxy', true);` it will respect `X-Forwarded-For` header. 
```js
module.exports = function (req, res, next) {
    if (req.session.userId === 'develop' && req.ip == '127.0.0.1') {
      return next();
    }
    res.status(403).send('Forbidden: Development access only');
  };
```

Flag: `TFCCTF{3at_sl1P_h4Ck_r3p3at_5af9f1}`

Solved by: benkyou
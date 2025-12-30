# Confessions

Challenge author: benkyou

Description: Inspired by uni confessions page, I vibecoded one for CTF players.

Flag: RE:CTF{XsS_j0uZu_D3sU_neee~owo!}

# Solution

I made this challenge based on a couple techniques we learned throughout the year playing CTFs at RE:UN10N. If you look at the challenge setup, we have a front facing web application, an admin bot, and an internal FTP server. The flag.txt is uploaded to the server by the bot during startup through `setFlag()`. If you look at the FTP server code, it's also misconfigured for anonymous access. Further, the admin bot is using Firefox so we need to target Firefox during testing.

The web app lets you create new confessions and view them. You may think you'd need to get an XSS here and submit to the admin bot but there are a couple of steps here.

1. In /app/index.js the confession is sanitized using DOMPurify server-side before it is pushed to the FTP server so normal XSS payloads won't trigger when it's fetched from the server and rendered.

```js
app.post('/save', requireLogin, async (req, res) => {
    const content = req.body.content || '';

    const DOMPurify = createDOMPurify(new JSDOM('').window);
    const sanitized = DOMPurify.sanitize(content, { ALLOW_ARIA_ATTR: false, ALLOW_DATA_ATTR: false });
```

The DOMPurify version used is not vulnerable to any known bypasses.

2. You may notice that the Content-Type header is missing the charset value when the confession is rendered to the user. This is shown by this block in the code.

```js
app.get('/confession/:id', async (req, res) => {
...
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.write(html);
    res.end();
```

We have a problem here, because when charset is missing in Content-Type header, the browser will try to guess the charset and this allows us to bypass DOMPurify using ISO-2022-JP encoding. We have an encoding differential :D

> This only works on Firefox. If you tested in on Chromium browsers, this technique will fail because ISO-2022-JP auto-detection has been patched.

We have a DOMPurify bypass, but the flag is still on the FTP server and not with the admin bot.
To exploit this, you can send FTP commands to the internal FTP server using the admin bot (since they are on the same internal network) using your XSS. This is possible because FTP is quite lax, and will gladly process any data that gets sent to it as long as it's formatted with line feeds properly. So you can not use an FTP client, and still be able to talk to it. The HTTP headers will break the FTP syntax, but FTP server will still gladly parse the FTP commands and accept them :D

Finally, to exfiltrate the flag you need to leverage FTP active mode to make the server retrieve the flag and send it back to you.

References
- https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/
- https://ctftime.org/writeup/29641
- https://slacksite.com/other/ftp.html#actexample
- https://chromium-review.googlesource.com/c/chromium/src/+/6378605
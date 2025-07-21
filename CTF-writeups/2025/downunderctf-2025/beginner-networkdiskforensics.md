## Solution:
```
sudo modprobe nbd max_part=8
sudo nbd-client chal.2025.ductf.net 30016 /dev/nbd0 -name root -persist
sudo mkdir /mnt/ductf
sudo mount -t ext4 /dev/nbd0 /mnt/ductf
```
flag will be in /mnt/ductf/flag.jpg

Flag:  `DUCTF{now_you_know_how_to_use_nbd_4y742rr2}`

Solved by: vicevirus
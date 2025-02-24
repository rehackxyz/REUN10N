# arclboth

Solved by: @vicevirus
### Question:
I heard [Arc'blroth](https://bulr.boo/) was writing challenges for LA CTF. Wait, is it arc'blroth or arcl broth?
### Solution:
sqlite truncation with \x00
```sqlite
payload = {
    "username": "admin\x00",
    "password": "ssssssss"
}
```

**Flag:** `lactf{bulri3v3_it_0r_n0t_s3cur3_sqlit3_w4s_n0t_s3cur3}`


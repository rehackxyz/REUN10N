# Solution
```
#!/usr/bin/env python3
from fractions import Fraction
from hashlib import sha256
import math

def parse_points(filename):
    """Parses the x and y values from the points file."""
    points = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            # line format: x=..., y=num/den
            parts = line.strip().split(", ")
            x_val = int(parts[0].split("=")[1])
            y_val = Fraction(parts[1].split("=")[1])
            points.append((x_val, y_val))
    return points

def solve():
    print("[*] Reading points...")
    points = parse_points("points.txt")
    x1, y1 = points[0]
    x2, y2 = points[1]

    print("[*] Calculating a^2...")
    # Formula: a^2 = (y2*x2^2 - y1*x1^2) / (y1 - y2)
    
    numerator = (y2 * (x2**2)) - (y1 * (x1**2))
    denominator = y1 - y2
    
    a_squared = numerator / denominator
    
    # Since a_squared is a Fraction, we take the sqrt of num and den separately
    # a = p/q  => a^2 = p^2/q^2
    print("[*] Calculating sqrt(a^2) to recover a...")
    p = math.isqrt(a_squared.numerator)
    q = math.isqrt(a_squared.denominator)
    
    a = Fraction(p, q)
    
    # Sanity check
    if a * a != a_squared:
        print("[-] Error: Perfect square root not found. Check precision.")
        return

    print(f"[+] Recovered a: {str(a)[:50]}...") # Print first 50 chars

    # Reconstruct Key
    print("[*] Generating key...")
    key_payload = f"{a.numerator}/{a.denominator}"
    key = sha256(key_payload.encode()).digest()

    # Decrypt
    print("[*] Decrypting ciphertext...")
    with open("ciphertext.hex", "r") as f:
        ct_hex = f.read().strip()
        ct = bytes.fromhex(ct_hex)

    flag = bytes([ct[i] ^ key[i % len(key)] for i in range(len(ct))])
    
    try:
        print(f"\n[SUCCESS] Flag: {flag.decode()}")
    except UnicodeDecodeError:
        print(f"\n[PARTIAL] Raw bytes (decoding failed): {flag}")

if __name__ == "__main__":
    solve()

```

Flag:nullctf{I_w0nderwh0!s_th3_w!tch_0f_Agn3s!?_6920686f7065207468652063746620776173206e696365}

Solved by: ha1qal

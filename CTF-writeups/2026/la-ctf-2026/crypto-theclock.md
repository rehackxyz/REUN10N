# crypto - the-clock

```
import math
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Given values
xg = 13187661168110324954294058945757101408527953727379258599969622948218380874617
yg = 5650730937120921351586377003219139165467571376033493483369229779706160055207

xA = 13109366899209289301676180036151662757744653412475893615415990437597518621948
yA = 5214723011482927364940019305510447986283757364508376959496938374504175747801

xB = 1970812974353385315040605739189121087177682987805959975185933521200533840941
yB = 12973039444480670818762166333866292061530850590498312261363790018126209960024

ct_hex = "d345a465538e3babd495cd89b43a224ac93614e987dfb4a6d3196e2d0b3b57d9"

def recover_p():
    def e(x, y):
        return x*x + y*y - 1
    g = math.gcd(e(xg, yg), e(xA, yA))
    g = math.gcd(g, e(xB, yB))
    return g

p = recover_p()
print("[+] p =", p)

def mul(P, Q):
    x1, y1 = P
    x2, y2 = Q
    return ((x1*y2 + y1*x2) % p, (y1*y2 - x1*x2) % p)

ID = (0, 1)

def inv(P):
    x, y = P
    return ((-x) % p, y)  # conjugate; works since norm=1

def pow_elem(P, n):
    R = ID
    B = P
    while n > 0:
        if n & 1:
            R = mul(R, B)
        B = mul(B, B)
        n >>= 1
    return R

g = (xg % p, yg % p)
A = (xA % p, yA % p)
B = (xB % p, yB % p)

n = p + 1  # order of norm-1 subgroup

# Factor n by trial division (works here because it's smooth)
def factor_smooth(N, bound=2_000_000):
    m = N
    fac = {}
    d = 2
    while d*d <= m and d <= bound:
        while m % d == 0:
            fac[d] = fac.get(d, 0) + 1
            m //= d
        d = 3 if d == 2 else d + 2
    if m != 1:
        fac[m] = fac.get(m, 0) + 1
    return fac

factors = factor_smooth(n)
print("[+] factors of p+1:", factors)

def dlog_prime_power(h, g, q, e, n):
    # Solve g^x = h mod q^e using standard Pohlig–Hellman lifting
    gq = pow_elem(g, n // q)  # order q
    table = {}
    cur = ID
    for k in range(q):
        table[cur] = k
        cur = mul(cur, gq)

    x = 0
    qpow = 1
    for _ in range(e):
        gx = pow_elem(g, x)
        t = mul(h, inv(gx))
        exp = n // (qpow * q)
        tj = pow_elem(t, exp)  # in subgroup of order q
        dj = table[tj]
        x += dj * qpow
        qpow *= q
    return x

def crt(congruences):
    M = 1
    for _, m in congruences:
        M *= m
    x = 0
    for a, m in congruences:
        Mi = M // m
        invMi = pow(Mi, -1, m)
        x = (x + a * Mi * invMi) % M
    return x, M

def pohlig_hellman(h, g, factors, n):
    congr = []
    for q, e in factors.items():
        congr.append((dlog_prime_power(h, g, q, e, n), q**e))
    x, _ = crt(congr)
    return x

alice_secret = pohlig_hellman(A, g, factors, n)
bob_secret   = pohlig_hellman(B, g, factors, n)

shared = pow_elem(A, bob_secret)
key = md5(f"{shared[0]},{shared[1]}".encode()).digest()

ct = bytes.fromhex(ct_hex)
pt = AES.new(key, AES.MODE_ECB).decrypt(ct)
pt = unpad(pt, 16)

print("[+] flag =", pt.decode())
```

Flag:` lactf{t1m3_c0m3s_f4r_u_4all}`

Solved by: yappare
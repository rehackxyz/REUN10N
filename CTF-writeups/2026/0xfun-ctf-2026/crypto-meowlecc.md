# crypto - MeOwl ECC

https://chatgpt.com/share/698ee2af-4b20-8009-9e05-dce7330603e4

FLAG:`0xfun{n0n_c4n0n1c4l_l1f7s_r_c00l}`
#!/usr/bin/env python3
import re, random, hashlib
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes

# ---------- parse chall.py + output.txt ----------
with open("chall.py","r",encoding="utf-8") as f:
    chall = f.read()
with open("output.txt","r",encoding="utf-8") as f:
    out = f.read()

def grab_int(name, src):
    m = re.search(rf"{name}\s*=\s*(\d+)", src)
    if not m:
        raise ValueError(f"missing {name}")
    return int(m.group(1))

p  = grab_int("p",  chall)
a0 = grab_int("a",  chall)
b0 = grab_int("b",  chall)
Px = grab_int("Px", chall); Py = grab_int("Py", chall)
Qx = grab_int("Qx", chall); Qy = grab_int("Qy", chall)

aes_iv_hex = re.search(r'aes_iv\s*=\s*"([0-9a-fA-F]+)"', chall).group(1)
des_iv_hex = re.search(r'des_iv\s*=\s*"([0-9a-fA-F]+)"', chall).group(1)
ct_hex = re.search(r'ciphertext\s*=\s*([0-9a-fA-F]+)', out).group(1)

aes_iv = bytes.fromhex(aes_iv_hex)
des_iv = bytes.fromhex(des_iv_hex)
ct = bytes.fromhex(ct_hex)

# ---------- EC over F_p (affine) for verification ----------
O = None
def inv_mod(x, m): return pow(x, -1, m)

def ec_add(P, Q):
    if P is None: return Q
    if Q is None: return P
    x1,y1 = P
    x2,y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P != Q:
        lam = ((y2 - y1) * inv_mod((x2 - x1) % p, p)) % p
    else:
        lam = ((3*x1*x1 + a0) * inv_mod((2*y1) % p, p)) % p
    x3 = (lam*lam - x1 - x2) % p
    y3 = (lam*(x1 - x3) - y1) % p
    return (x3,y3)

def ec_mul(k, P):
    R = None
    A = P
    while k:
        if k & 1:
            R = ec_add(R, A)
        A = ec_add(A, A)
        k >>= 1
    return R

P = (Px,Py); Q = (Qx,Qy)

# anomalous sanity: P is killed by p
assert ec_mul(p, P) is None

# ---------- Hensel lift for y mod p^2 ----------
N = p*p
def hensel_lift_y(x, y0, a, b):
    f = (x*x*x + a*x + b) % N
    diff = (f - (y0*y0) % N) % N
    delta = (diff // p) % p
    t = (delta * inv_mod((2*y0) % p, p)) % p
    return (y0 + t*p) % N

# ---------- Jacobian arithmetic mod p^2 ----------
INF = (1,1,0)
def is_inf(R): return (R[2] % N) == 0

def jac_double(R, a):
    X1,Y1,Z1 = R
    if is_inf(R) or (Y1 % N) == 0:
        return INF
    Y1sq = (Y1*Y1) % N
    S = (4 * X1 * Y1sq) % N
    Z1sq = (Z1*Z1) % N
    Z1_4 = (Z1sq*Z1sq) % N
    M = (3 * X1 * X1 + a * Z1_4) % N
    X3 = (M*M - 2*S) % N
    Y1_4 = (Y1sq*Y1sq) % N
    Y3 = (M*(S - X3) - 8*Y1_4) % N
    Z3 = (2 * Y1 * Z1) % N
    return (X3,Y3,Z3)

def jac_add(R, S, a):
    if is_inf(R): return S
    if is_inf(S): return R
    X1,Y1,Z1 = R
    X2,Y2,Z2 = S
    Z1sq = (Z1*Z1) % N
    Z2sq = (Z2*Z2) % N
    U1 = (X1 * Z2sq) % N
    U2 = (X2 * Z1sq) % N
    Z1cb = (Z1sq * Z1) % N
    Z2cb = (Z2sq * Z2) % N
    S1 = (Y1 * Z2cb) % N
    S2 = (Y2 * Z1cb) % N
    H = (U2 - U1) % N
    r = (S2 - S1) % N
    if H == 0:
        if r == 0:
            return jac_double(R, a)
        return INF
    H2 = (H*H) % N
    H3 = (H2*H) % N
    U1H2 = (U1*H2) % N
    X3 = (r*r - H3 - 2*U1H2) % N
    Y3 = (r*(U1H2 - X3) - S1*H3) % N
    Z3 = (H * Z1 * Z2) % N
    return (X3,Y3,Z3)

def jac_mul(k, R, a):
    Qr = INF
    A = R
    while k:
        if k & 1:
            Qr = jac_add(Qr, A, a)
        A = jac_double(A, a)
        k >>= 1
    return Qr

def phi_from_R(R):
    # local parameter t = -x/y = -(X*Z)/Y  (x=X/Z^2, y=Y/Z^3)
    X,Y,Z = R
    t = (-X * Z) % N
    t = (t * inv_mod(Y % N, N)) % N
    if t % p != 0:
        return None
    return (t // p) % p

# ---------- Smart-style search for a workable non-canonical lift ----------
random.seed(0)

d = None
while True:
    # lift curve: a' = a + A*p, b' = b + B*p  (mod p^2)
    A = random.randrange(0, 200)
    B = random.randrange(0, 200)
    a = (a0 + A*p) % N
    b = (b0 + B*p) % N

    # lift points by shifting x by u*p (changes the section)
    uP = random.randrange(0, 200)
    uQ = random.randrange(0, 200)
    xP = (Px + uP*p) % N
    xQ = (Qx + uQ*p) % N
    yP = hensel_lift_y(xP, Py, a, b)
    yQ = hensel_lift_y(xQ, Qy, a, b)

    Pj = (xP, yP, 1)
    Qj = (xQ, yQ, 1)

    Rp = jac_mul(p, Pj, a)
    Rq = jac_mul(p, Qj, a)
    if is_inf(Rp) or is_inf(Rq):
        continue

    phiP = phi_from_R(Rp)
    phiQ = phi_from_R(Rq)
    if phiP in (None, 0) or phiQ is None:
        continue

    cand = (phiQ * inv_mod(phiP, p)) % p
    if ec_mul(cand, P) == Q:
        d = cand
        break

# ---------- decrypt ----------
aes_key = hashlib.sha256(long_to_bytes(d) + b"MeOwl::AES").digest()[:16]
des_key = hashlib.sha256(long_to_bytes(d) + b"MeOwl::DES").digest()[:8]

mid = unpad(DES.new(des_key, DES.MODE_CBC, iv=des_iv).decrypt(ct), 8)
pt  = unpad(AES.new(aes_key, AES.MODE_CBC, iv=aes_iv).decrypt(mid), 16)

print("d =", d)
print("flag =", pt.decode())

Solved by: ha1qal
# Solution
```
def read_states(path="keystream_leak.txt"):
    states = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            states.append(int(line))
    return states

def bitvec32(x):
    return [(x >> k) & 1 for k in range(32)]

def solve_gf2(M, y):
    M = [row[:] for row in M]
    y = y[:]
    m = len(M)
    if m == 0:
        return []

    n = len(M[0])
    pivots = [-1] * n
    row = col = 0

    while row < m and col < n:
        pivot = None
        for r in range(row, m):
            if M[r][col]:
                pivot = r
                break
        if pivot is None:
            col += 1
            continue

        if pivot != row:
            M[row], M[pivot] = M[pivot], M[row]
            y[row], y[pivot] = y[pivot], y[row]

        pivots[col] = row

        for r in range(row + 1, m):
            if M[r][col]:
                M[r] = [a ^ b for a, b in zip(M[r], M[row])]
                y[r] ^= y[row]

        row += 1
        col += 1

    for r in range(row, m):
        if any(M[r]) and y[r]:
            raise ValueError("No solution in GF(2)")

    u = [0] * n
    for col in range(n - 1, -1, -1):
        r = pivots[col]
        if r == -1:
            continue  # free variable, leave 0
        s = y[r]
        for c2 in range(col + 1, n):
            if M[r][c2] and u[c2]:
                s ^= 1
        u[col] = s

    return u

def recover_A_B(states):
    X = [bitvec32(s) for s in states[:-1]]  # S[n]
    Y = [bitvec32(s) for s in states[1:]]   # S[n+1]
    m = len(X)
    if m == 0:
        raise ValueError("Need at least 2 states")

    A_rows_bits = []
    B_bits = []

    for bit in range(32):
        M = [x + [1] for x in X]  # append 1 for B's bit
        yb = [Y[i][bit] for i in range(m)]
        sol = solve_gf2(M, yb)
        row_bits = sol[:32]
        B_bit = sol[32]
        A_rows_bits.append(row_bits)
        B_bits.append(B_bit)

    # Pack row bits into 32-bit masks
    A_rows = []
    for row_bits in A_rows_bits:
        mask = 0
        for k, b in enumerate(row_bits):
            if b:
                mask |= (1 << k)
        A_rows.append(mask)

    B = 0
    for k, b in enumerate(B_bits):
        if b:
            B |= (1 << k)

    return A_rows, B

def parity32(x):
    x ^= x >> 16
    x ^= x >> 8
    x ^= x >> 4
    x &= 0xf
    return (0x6996 >> x) & 1  # precomputed parity table for 4 bits

def next_state(A_rows, B, s):
    y = 0
    for out_bit, row_mask in enumerate(A_rows):
        # dot product over GF(2) is just bitwise AND + parity
        v = row_mask & s
        p = parity32(v)
        b = (B >> out_bit) & 1
        if p ^ b:
            y |= (1 << out_bit)
    return y

def keystream_bytes(A_rows, B, s0, nbytes):

    s = s0
    out = bytearray()
    for _ in range(nbytes):
        out.append(s & 0xFF)
        s = next_state(A_rows, B, s)
    return bytes(out)

def decrypt(ciphertext: bytes, keystream: bytes) -> bytes:
    return bytes(c ^ k for c, k in zip(ciphertext, keystream))

if __name__ == "__main__":
    states = read_states("matrix/keystream_leak.txt")
    A_rows, B = recover_A_B(states)

    with open("matrix/cipher.txt", "rb") as f:
        ciphertext = f.read()
    
    ks = keystream_bytes(A_rows, B, states[0], len(ciphertext))
    plaintext = decrypt(ciphertext, ks)
    print(plaintext)
```
Flag: `pctf{mAtr1x_r3construct?on_!s_fu4n}`

Solved by: ukyovis

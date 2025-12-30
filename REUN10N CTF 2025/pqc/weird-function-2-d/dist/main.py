import random
import secrets
import hashlib
from func import custom_func

t = 128; n = 80; m = 100000; noise = 0.18; k = 10

FLAG = open("flag.txt", "rb").read().strip()

seed = secrets.randbits(32)
random.seed(seed)

f = open("output.txt", "w")

def generate_row():
    return random.sample(range(n), k)

choices = [secrets.randbits(1) for _ in range(t)]
stream = hashlib.shake_128(bytes(choices)).digest(len(FLAG))
encrypted_flag = bytes(a ^ b for a, b in zip(FLAG, stream))

f.write(f'seed = {seed}\n')
f.write(f'encrypted_flag = {encrypted_flag.hex()}\n')

for i in range(128):
    s = [secrets.randbits(1) for _ in range(n)]
    e = [1 if secrets.randbelow(100) < noise * 100 else 0 for _ in range(m)]
    val = [[s[j] for j in generate_row()] for _ in range(m)]
    b = [(e[j] + custom_func(val[j])) % 2 for j in range(m)]
    if choices[i] == 1:
        f.write(''.join(map(str,b)) + '\n')
    else:
        b_random = [secrets.randbits(1) for _ in range(m)]
        f.write(''.join(map(str,b_random)) + '\n')
        
f.close()

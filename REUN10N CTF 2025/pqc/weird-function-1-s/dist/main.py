import random
import secrets
import hashlib
from func import custom_func

t = 10; n = 80; m = 6000; k = 10

FLAG = open("flag.txt", "rb").read().strip()

seed = secrets.randbits(32)
random.seed(seed)

f = open("output.txt", "w")

def generate_row():
    return random.sample(range(n), k)

s = [[secrets.randbits(1) for _ in range(n)] for _ in range(t)]
stream = hashlib.shake_128(bytes(sum(s, []))).digest(len(FLAG))
encrypted_flag = bytes(a ^ b for a, b in zip(FLAG, stream))

f.write(f'seed = {seed}\n')
f.write(f'encrypted_flag = {encrypted_flag.hex()}\n')

for i in range(t):
    val = [[s[i][j] for j in generate_row()] for _ in range(m)]
    b = [custom_func(val[j]) for j in range(m)]
    f.write(''.join(map(str,b)) + '\n')
        
f.close()

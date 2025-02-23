# RSaaS

Solved by: @w6rstaimn
### Question:
Tired of doing RSA on your own? Try out my new service!
### Solution:
```python
from pwn import remote, log
from Crypto.Util.number import isPrime, getPrime
import sys

def prime():
    lower_bound = 2**63
    upper_bound = 2**64
    k = lower_bound // 65537
    if lower_bound % 65537:
        k += 1

    while True:
        p = k * 65537 + 1
        if p >= upper_bound:
            break  #
        if isPrime(p):
            return p
        k += 1

    return None

def main():
    io = remote("chall.lac.tf", 31176)

    io.recvuntil("Input p: ")

    p = prime()
    if p is None:
        log.error("Could not find a suitable prime.")
        sys.exit(1)
    log.info("Chosen prime p: {}".format(p))


    io.sendline(str(p))
    io.recvuntil("Input q: ")

    q = getPrime(64)
    while not (2**63 < q < 2**64) or q == p:
        q = getPrime(64)
    log.info("Chosen prime q: {}".format(q))
    io.sendline(str(q))
    flag = io.recvall(timeout=5)
    print(flag.decode(errors="replace"))

if __name__ == "__main__":
    main()
```

**Flag:**`lactf{actually_though_whens_the_last_time_someone_checked_for_that}`


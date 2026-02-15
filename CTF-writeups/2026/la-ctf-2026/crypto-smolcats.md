# crypto - smol cats

```
sage: n = 1317386120324336772142665640374224731368166553310018392382389
....: e = 65537
....: c = 167051788301039816934495994054701938925231864306729761146716
....:
....: factors = factor(n)
....: p, q = [f[0] for f in factors]
....:
....: phi = (p - 1) * (q - 1)
....: d = inverse_mod(e, phi)
....:
....: m = power_mod(c, d, n)
....: print(m)
```

```
└─$ nc chall.lac.tf 31224
  /\_/\
 ( o.o )
  > ^ <

*meow* Welcome to my cat cafe!
I'm a hungry kitty and I've hidden my treats in a secret place.
I will let you know where I hid them if you can defeat my encryption >.<
I encrypted the number of treats I want with RSA... but my paws are small,
so I used tiny primes. *purrrrr*

n = 1536984001825708370880043145528773187168217805841460417687539
e = 65537
c = 394581534626118175867784582356104955640752482218580177810941

*mrrrow?* How many treats do I want? 1463751382327279760473997685788574681644327069587660201573018
*PURRRRRR* You got it right! You may pet me now.
Here's your reward, human:
lactf{sm0l_pr1m3s_4r3_n0t_s3cur3}
```
SOLVED by hikki

Solved by: yappare
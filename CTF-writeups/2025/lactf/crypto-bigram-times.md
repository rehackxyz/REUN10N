# bigram-times

Solved by: @hikki
### Question:
Its time to times some bigrams!
### Solution:
1. Create dictionary of all possible characters shift maps the shifted flag
2. Filter the candidates by removing notflag char from candidates 
3. The remaining candidates is the flag

```python
from itertools import product

characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}~_"
shifted_flag = "jlT84CKOAhxvdrPQWlWT6cEVD78z5QREBINSsU50FMhv662W"
not_the_flag = "mCtRNrPw_Ay9mytTR7ZpLJtrflqLS0BLpthi~2LgUY9cii7w"
also_not_the_flag = "PKRcu0l}D823P2R8c~H9DMc{NmxDF{hD3cB~i1Db}kpR77iU"

def bigram_multiplicative_shift(bigram):
    """Applies the given transformation on a two-character bigram."""
    assert len(bigram) == 2
    pos1 = characters.find(bigram[0]) + 1
    pos2 = characters.find(bigram[1]) + 1
    shift = (pos1 * pos2) % 67
    return characters[((pos1 * shift) % 67) - 1] + characters[((pos2 * shift) % 67) - 1]

bigram_dict = {} 
for c1 in characters:
    for c2 in characters:
        transformed = bigram_multiplicative_shift(c1 + c2)
        if transformed not in bigram_dict:
            bigram_dict[transformed] = []
        bigram_dict[transformed].append(c1 + c2)

shifted_bigrams = [shifted_flag[i:i+2] for i in range(0, len(shifted_flag), 2)]
candidates = [bigram_dict.get(bigram, []) for bigram in shifted_bigrams]

not_the_flag_bg = [not_the_flag[i:i+2] for i in range(0, len(not_the_flag), 2)]
also_not_the_flag_bg = [also_not_the_flag[i:i+2] for i in range(0, len(also_not_the_flag), 2)]
invalid_bg = set(not_the_flag_bg + also_not_the_flag_bg)

filtered = []
for bigram_options in candidates:
    filtered.append([bg for bg in bigram_options if bg not in invalid_bg])

possible_flags = [''.join(p) for p in product(*filtered) if ''.join(p).startswith("lactf{")]

print("Possible flag(s):")
for flag in possible_flags:
    print(flag)
```

**Flag:** `lactf{mULT1pl1cAtiV3_6R0uPz_4rE_9RE77y_5we3t~~~}`


# patricks-paraflag

Solved by: @arifpeycal
### Question:
I was going to give you the flag, but I dropped it into my parabox, and when I pulled it back out, it got all scrambled up!

Can you recover the flag
### Solution:
Get encrypted flag from ELF file, extract even index and odd index chars. concatenate both to get the flag

```python
def reverse_paradoxified(encrypted_flag):
    half_length = len(encrypted_flag) // 2
    part1 = encrypted_flag[::2]  
    part2 = encrypted_flag[1::2]  
    original_flag = part1 + part2  
    return original_flag

encrypted_flag = "l_alcotsft{_tihne__ifnlfaign_igtoyt}"
original_flag = reverse_paradoxified(encrypted_flag)

print(original_flag)
```

**Flag:**`lactf{the_flag_got_lost_in_infinity}`
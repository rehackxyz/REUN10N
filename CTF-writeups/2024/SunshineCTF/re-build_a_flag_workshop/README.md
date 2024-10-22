# Build A Flag Workshop

Solved by: @ks, @0x251e, @OS1R1S, @n3r

## Question:
Don't you ever want to customize your very own flag? Well now you can with Chompy's brand new Build-A-Flag-Workshop (patent pending)!

## Solution:
@0x251e progress:
1. from ida search string sun lead to `sub_19C0`
2. notice between `decide` and `chompy` have md5 subfunction which check memory address of `xmmword_4010`
3. run debugger,
```
break *0x1220
run
info proc mappings
x/16xb 0x555555558010
```

@ks said:
so basically you need to satisfy 3 things
1. first part of the flag = the wordlist that contains `decide`
2. 2nd part of the flag = md5 value (`gandalf`)
3. 3rd part of the flag = `chompy` 

**Flag:** `sun{all_we_have_to_decide_is_what_to_do_with_the_time_given_to_us-gandalf-chompy}`

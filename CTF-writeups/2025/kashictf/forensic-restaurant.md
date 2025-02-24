# Restaurant

Solved by: @OS1R1S
### Question:
I just asked for my favourite pasta and they gave me this. Are these guys STUPID? Maybe in the end they may give me something real. (Wrap the text in `KashiCTF{}`)

![[paste-forenisc.png]]

### Solution:
1. Hexdump inside image this patterns: `baabaaabbbaabaab abbababaaaabaaba aaaaabaabaaaaaab aaaaaaaababaabab aababaababababba aaabaabbababbaba baababaaaabbaaaa bba0`
2. Decode using bacon cipher and got this unique string `THEYWEREREALLLLYCOOKING`

**Flag:** `KashiCTF{THEYWEREREALLLLYCOOKING}`

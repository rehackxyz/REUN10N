# In Plain Sight

Solved by: @If-Modified-Since

## Question:
Barely hidden tbh..


## Solution:
1 - `strings meow.jpg` and found `YoullNeverGetThis719482 flag.pngUT`
2 - `binwalk -e meow.jpg`
3 - `cd _meow.jpg.extracted`
4 - `unzip 20BA6E.zip `(password = YoullNeverGetThis719482 )
5 - the `flag.png` need to superimposed, then get the flag


**Flag:** `INTIGRITI{w4rmup_fl46z}`

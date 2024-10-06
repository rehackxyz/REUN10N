# Treasure Hunt

Solved by: @OS1RIS

## Question:

I like colors and solving puzzles. What is better than having an app that brings both of them together?
flag format: wrap your flag using ironCTF{}

## Solution:

##### Solution #1:
1. Use apktool

```bash
$ $apktool -d TreasureHunt.apk
```

2. grep or read line by line


##### Solution #2:
1. Use jadx
2. navigate : res/layout/activity\_main.xml : `3ver_h3ard`
3. navigate : res/values/strings.xml : `0f_4ndro1d_r3v?`

**Flag:** `ironCTF{3ver_h3ard_0f_4ndro1d_r3v}`


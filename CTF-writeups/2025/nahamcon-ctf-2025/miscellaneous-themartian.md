# Solution

Strings the file and can see multiple jpg files  
binwalk extract the challenge file.  

```
$ file *
30DF: bzip2 compressed data, block size = 900k
34:   JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 968x118, components 3
8080: bzip2 compressed data, block size = 900k
957D: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 968x118, components 3
C628: bzip2 compressed data, block size = 900k
```

`mv 34 34.jpg` open as jpg and got flag  

Flag:`flag{0db031ac265b3e6538aff0d9f456004f}`

Solved by: zeqzoq

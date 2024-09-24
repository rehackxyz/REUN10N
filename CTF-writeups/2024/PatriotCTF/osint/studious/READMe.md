# Studious

Solved by: @okay

- Category: OSINT
- Description:

How much was tuition in for GWU graduate per credit hour for the 1998-1999 school year? Flag will be amount with just a period, like PCTF{1050.75} if it were $1,050.75.

NOTE: George Washington University, not George Mason University.

### Solution:

- Use wayback machine to travel back in time

Answer: [https://web.archive.org/web/20031224140534/http://www.gwu.edu/~media/pressreleases/tuition.html](https://web.archive.org/web/20031224140534/http://www.gwu.edu/~media/pressreleases/tuition.html)

This line: 
```
Tuition and fees for on-campus graduate students will be $714.50 per credit hour and GW Law School tuition and fees will increase 4% to $23,955.
```

**Flag:** `PCTF{714.50}`

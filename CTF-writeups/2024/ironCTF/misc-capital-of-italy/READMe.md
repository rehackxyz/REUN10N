# Capital of Italy

Solved by: @vicevirus

## Question:

Nothing... Just a simple pyjail.

## Solution:

1. After run a script to test allowed characters, only two characters are allowed: `(` and `)`
2. Based on the challenge title, it suggest italic font
3. With this [Italic Text Generator](https://lingojam.com/ItalicTextGenerator), we can use to input `help()` and it will convert it to italic `𝘩𝘦𝘭𝘱()`
4. Run `𝘩𝘦𝘭𝘱()` then run `__main__`

```bash
$ nc misc.1nf1n1ty.team 30010
WELCOME :)
𝘩𝘦𝘭𝘱()

Welcome to Python 3.10's help utility!

If this is your first time using Python, you should definitely check out
the tutorial on the internet at https://docs.python.org/3.10/tutorial/.

Enter the name of any module, keyword, or topic to get help on writing
Python programs and using Python modules.  To quit this help utility and
return to the interpreter, just type "quit".

To get a list of available modules, keywords, symbols, or topics, type
"modules", "keywords", "symbols", or "topics".  Each module also comes
with a one-line summary of what it does; to list the modules whose name
or summary contain a given string such as "spam", type "modules spam".

help> __main__
Help on module __main__:

NAME
    __main__

DATA
    __annotations__ = {}
    blacklist = ' \t\n\r\x0b\x0c0123456789abcdefghijklmnopqrstuvwxyzABCDEF...
    breakpoint = 'breakpoint'
    chars = ']'
    data = '𝘩𝘦𝘭𝘱()'
    ffiivVIxistivIX = 'ironCTF{R0M4N_T1mes}'

FILE
    /chal/pwn
```

**Flag:** `ironCTF{R0M4N\_T1mes}`


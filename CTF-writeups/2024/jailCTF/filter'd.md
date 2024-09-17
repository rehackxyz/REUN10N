# filter'd 

Solved by: @vicevirus

- Category: pyjail, introductory, golf
- Description: i asked the tech support guy for help with escaping this jail but all he said in his reply was "lmao u just got filter'd"...

### Solution:

1. First Input:
```
i=input;f(i())
```
2. Second Input:
```
M*=9;f(i())
```
3. Third Input:
```
print(open('flag.txt').read())
```

Flag: `jail{can_you_repeat_that_for_me?_aacb7144d2c}`



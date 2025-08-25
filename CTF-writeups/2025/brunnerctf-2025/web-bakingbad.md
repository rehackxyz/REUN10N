It gives a web interface with a textbox allowing users to enter an ingredient and it will give you a purity of it. From the description of the challenge, it says that it runs bash -c “ingredients” to have it processed. Thus, this is a command injection.

After many tries, noted that a break line (%0A) was enough to get shell working and `head`, `tail` and `ls` are maybe the only commands that worked so far. Using `ls` to get the directory structure and `head` and `tail` command to fetch the source code namely `quality.sh` and `index.php` was enough to get know the inner workings. There is a function that can be used but inaccessible to the user. Thus, again using `head` and `tail` to get the file but hit with slashes being blocked as well. Using `{PWD:0:1}` to fetch the slashes from first character of directory which is a slash, we can get the flag as follows.

Full url: <url>/?ingredient=%0Ahead%09-n%0910%09${PWD:0:1}flag.txt which translates to `head    -n    10    /flag.txt`

Flag: brunner{d1d_1_f0rg37_70_b4n_s0m3_ch4rz?}

Solved by: jerit3787
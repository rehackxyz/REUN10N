# unknown

Solved by: @yappare

### Question
Some may call this junk. Me, I call them treasures.

### Solution:

1. Check the file type of the archieved zip file

```bash
$ file unknown.zip
unknown.zip: gzip compressed data, from Unix, original size modulo 2^32 10240
```

Here it shows is a gzip compressed data, which suppose to end with gzip file extension. We can unarchieve without changing the file extension

2. Use 7zip to unarchieve the file

```bash
$ 7z x unknown.zip

7-Zip [64] 17.05 : Copyright (c) 1999-2021 Igor Pavlov : 2017-08-28
p7zip Version 17.05 (locale=en_US.UTF-8,Utf16=on,HugeFiles=on,64 bits,8 CPUs x64)

Scanning the drive for archives:
1 file, 185 bytes (1 KiB)

Extracting archive: unknown.zip
WARNING:
unknown.zip
Can not open the file as [zip] archive
The file is open as [gzip] archive

--
Path = unknown.zip
Open WARNING: Can not open the file as [zip] archive
Type = gzip
Headers Size = 10

Everything is Ok

Archives with Warnings: 1
Size:       10240
Compressed: 185
```

3. Check the unknown file after extracting it

```bash
$ file unknown
unknown: POSIX tar archive (GNU)
```

It shows a tar archieve file, since it is not encrypted, we can cat out as strings to view the contents.

4. Strings the unknown file
```bash
$ strings unknown
unknown/
0000755
0001750
0001750
00000000000
14675573136
011572
ustar
mbund
mbund
unknown/flag.txt
0000644
0001750
0001750
00000000043
14675573136
013241
ustar
mbund
mbund
bctf{f1l3_3x73n510n5_4r3_n07_r34l}
```

**Flag:** `bctf{f1l3_3x73n510n5_4r3_n07_r34l}`


# reduce_recycle

Solved by: @yappare

### Question
I forgot the randomly generated 12-character password I used to encrypt these files.... is there anything you can do to help me get my flag back??

### Solution:

1. Identify the contents in the zip file and 7z file

```bash
Archive:  dogs_wearing_tools.zip
 Length   Method    Size  Cmpr    Date    Time   CRC-32   Name
--------  ------  ------- ---- ---------- ----- --------  ----
 1817550  Stored  1817550   0% 2024-09-01 19:38 346673b4  1.png
 1830967  Stored  1830967   0% 2024-09-01 19:38 0fe18ee0  2.png
   94416  Stored    94416   0% 2024-09-01 19:38 9c62018f  3.png
 1210542  Stored  1210542   0% 2024-09-01 19:36 ba690f9b  4.png
--------          -------  ---                            -------
 4953475          4953475   0%                            4 files
```

The method `Stored` indicates no compression for all the files. 

```bash
exiftool important_flags.7z
ExifTool Version Number         : 12.96
File Name                       : important_flags.7z
Directory                       : .
File Size                       : 186 bytes
File Modification Date/Time     : 2024:09:30 18:27:19+00:00
File Access Date/Time           : 2024:09:30 18:28:07+00:00
File Inode Change Date/Time     : 2024:09:30 18:27:28+00:00
File Permissions                : -rw-r--r--
File Type                       : 7Z
File Type Extension             : 7z
MIME Type                       : application/x-7z-compressed
File Version                    : 7z v0.04
Modify Date                     : 2024:09:19 01:32:35+00:00
Archived File Name              : flag.txt
```

In the 7z file it has flag.txt. We have to crack open the zip file in order to open the 7z file for the flag.

2. Use bkcrack to crack zip file

Here is a short tutorial reference for bkcrack: [https://github.com/kimci86/bkcrack/blob/master/example/tutorial.md](https://github.com/kimci86/bkcrack/blob/master/example/tutorial.md)

Since the files is not compressed, we can have a plaintext that contain the first 12 bytes of the file. Since all the files are PNG and the magic bytes are 89504E470D0A1A0A0000000D

```bash
$ echo -n "89504E470D0A1A0A0000000D" | xxd -r -p > plaintext.bin
```

Next using bkcrack to get the keys 

```bash
$ ./bkcrack -C ../dogs_wearing_tools.zip -c 1.png -p plaintext.bin
bkcrack 1.7.0 - 2024-05-26
[19:06:41] Z reduction using 5 bytes of known plaintext
100.0 % (5 / 5)
[19:06:41] Attack on 1190986 Z values at index 6
Keys: adf73413 6f6130e7 0cfbc537
7.7 % (91728 / 1190986)
Found a solution. Stopping.
You may resume the attack with the option: --continue-attack 91728
[19:08:52] Keys
adf73413 6f6130e7 0cfbc537
```

We can remove the password into a new zip file
```bash
./bkcrack -C ../dogs_wearing_tools.zip -k adf73413 6f6130e7 0cfbc537 -D without_pass.zip
```

After unzipping the unencrypted file, we found 4 images of dogs. 

3. Crack open the 7z file

Based on the question, the challenge stated that 12 characters password is used to encrypted these two files. 

First we have to recover the original password from the keys just now

```bash
./bkcrack -k adf73413 6f6130e7 0cfbc537 --bruteforce ?a --length 12
bkcrack 1.7.0 - 2024-05-26
[19:22:31] Recovering password
length 12...
Password: 2n3Ad3&ZxDvV (as bytes: 32 6e 33 41 64 33 26 5a 78 44 76 56)
Some characters are not in the expected charset. Continuing.
100.0 % (3844 / 3844)
[19:22:41] Could not recover password
```
We got the password `2n3Ad3&ZxDvV`

```bash
$ 7z x important_flags.7z -p"2n3Ad3&ZxDvV"
```

**Flag:** `bctf{wH1ch_d0g_w4s_youR_FaVOr1t3}`



# pwn - Average Heap Challenge

1: Allocate a player with a long name so the message write overflows into the next chunk's metadata

2: Overwrite the adjacent chunk's size header from 0x50to 0x71

3. Free the corrupted chunk (forcing it into the 0x70 Tcache bin) and reallocate it

4. Overwrite target with 0xdeadbeefcafebabe to get the flag

Solved by Jigenz

Solved by: yappare
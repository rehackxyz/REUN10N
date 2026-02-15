# rev - starless-c

```
$ file starless_c
starless_c: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, no section header
```

-ELF64: statically linked, no section headers, lots of PT_LOAD segments, entry found at 0x13370000 sbb jumpa intro "There is a flag in the binary."
-after intro ada jmp to "room" loop
-basically from one room to another room, our goal is to go to 0x42069000 sbb ada sendfile funciton which is the flag.
-can move with wasd, lastly use f to run after wasd mapping
-after knowing what to do, craft prompt to ai to search for the path
-after some try got dsdddswaasdwaaasdssawwdwddsawasassdddwsddwasaaaawwdwdddsawaasassdddwwdwasssaaawwdwwassdddssddwasaaawwddwdsaaawdasssddwsddwawaawasdddssawdwaaddwaaf

```
$ nc chall.lac.tf 32223
There is a flag in the binary.
  (The flag is a metaphor but also still a flag.)
  (The binary could rightly be considered a gimmick.)
dsdddswaasdwaaasdssawwdwddsawasassdddwsddwasaaaawwdwdddsawaasassdddwwdwasssaaawwdwwassdddssddwasaaawwddwdsaaawdasssd
dwsddwawaawasdddssawdwaaddwaaf
A person this far into a challenge has their path to follow. There were many paths, once, in a time that is past, lost many bytes and pages ago. Now there is only one path for you to choose. The path that leads to the flag.
lactf{starless_c_more_like_starless_0xcc}
```

Solved by Zeqzoq

Solved by: yappare
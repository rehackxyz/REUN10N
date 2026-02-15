# forensic - printed parts

when open. can see `flag.stl`
```
┌──(myenv)(osiris㉿ALICE)-[/mnt/c/Users/os1ris/Downloads]
└─$ strings 3D.gcode | grep -i "flag"
;MESH:flag.stl
;MESH:flag.stl
;MESH:flag.stl
;MESH:flag.stl
;MESH:flag.stl
;MESH:flag.stl
;MESH:flag.stl
---STRIP---
```

leave 'flag.stl' innit and remove all the `fill `part

(open .gcode using https://imagetostl.com/view-gcode-online#convert) 

from 
[this](https://media.discordapp.net/attachments/1471747812038279249/1471748068587212964/ImageToStl.com_3D.png?ex=699209f3&is=6990b873&hm=4c90f99d76ea9f1ea1e062bc71f2e7eaa9cb97cb165f921cc1ef29d581bfbde9&=&format=webp&quality=lossless)
to 
[this](https://cdn.discordapp.com/attachments/1471747812038279249/1471748097280442481/ImageToStl.com_flag_only.png?ex=699209fa&is=6990b87a&hm=f5768111066e031889ac768d5dfe2a9be7760cdb8946575ca4d385663930abb1&)
[and this](https://cdn.discordapp.com/attachments/1471747812038279249/1471748097804734626/ImageToStl.com_flag_only_1.png?ex=699209fa&is=6990b87a&hm=d22685f1815c6ec86af8366a1437303e57c23ce3e8c1cef8081ce98af16905e3&)
``` 
;START_OF_HEADER
;HEADER_VERSION:0.1
;FLAVOR:Griffin
;GENERATOR.NAME:Cura_SteamEngine
;GENERATOR.VERSION:5.10.2
;GENERATOR.BUILD_DATE:2025-07-28... (4 MB left)


flagout.gcode
```

flag: `0xfun{this_monkey_has_a_flag}`

Solved by: OS1R1S

## Attachments

![image.png](https://raw.githubusercontent.com/rehackxyz/REUN10N/main/CTF-writeups/2026/0xfun-ctf-2026/assets/printedparts-image.png)


Solved by: yappare

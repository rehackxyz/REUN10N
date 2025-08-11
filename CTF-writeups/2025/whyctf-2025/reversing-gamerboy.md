We're given a gameboy rom and the challenge is to enter the cheat code sequence to get the flag.

You can decompile gameboy roms in ghidra using [GhidraBoy](https://github.com/Gekkio/GhidraBoy).

Code is very simple, it parses our joypad inputs and compares it against the cheatcode (somewhere in memory). If we match 10 times, then we win. You can ignore `getFlag` implementation :)

To solve, I patched the `SUB C` instruction at `$03c7` to `SUB A` so we always get a zero. Then we need to modify [this ghidra script](https://raw.githubusercontent.com/ghidraninja/ghidra_scripts/refs/heads/master/export_gameboy_rom.py) to export the ROM.

```python
import re

def dump_block(file, name):
    block = currentProgram.memory.getBlock(name)
    file.write(block.getData().readAllBytes())

def rom_sorter(e):
    match = re.match(r"rom(\d+)", e)
    if match:
        return int(match.group(1))
    return float('inf')

blocks = currentProgram.memory.getBlocks()
names = []

for block in blocks:
    if block.getName().startswith("rom"):
        names.append(block.getName())

names = sorted(names, key=rom_sorter)

rom_file = str(askFile("Select target file", "Save ROM"))

with open(rom_file, "wb") as f:
    for n in names:
        dump_block(f, n)
```

Flag: `flag{0a94a34cf78309bf4aa7bc283e47fcd3}`

Solved by: benkyou
# rev - Unravel Me

create gdb script
```gdb
set pagination off
set confirm off
set verbose off

handle SIGSEGV pass nostop noprint
handle SIGILL  pass nostop noprint

# feed a long predictable arg so comparisons don't read past end
set args AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

python
import gdb

TEXT_START = 0x08049000
TEXT_SIZE  = 0x00008c28

# opcode for: mov eax, DWORD PTR [eax*4+0x81a7a80]
PAT = b"\x8b\x04\x85\x80\x7a\x1a\x08"

got = bytearray()

class XorBP(gdb.Breakpoint):
    def stop(self):
        try:
            a = int(gdb.parse_and_eval("*(unsigned char*)0x81fbff0"))
            b = int(gdb.parse_and_eval("*(unsigned char*)0x81fbff4"))
        except gdb.error:
            return False

        # We set argv[1] = 'A' * N, so real per-byte compares will have a == 0x41.
        if a == 0x41:
            got.append(b)
        return False  # auto-continue

# Set breakpoints on every occurrence of that table-lookup instruction in .text
inferior = gdb.selected_inferior()
mem = inferior.read_memory(TEXT_START, TEXT_SIZE).tobytes()

addrs = []
i = 0
while True:
    j = mem.find(PAT, i)
    if j == -1:
        break
    addrs.append(TEXT_START + j)
    i = j + 1

for a in addrs:
    XorBP(f"*0x{a:x}")

def on_exit(ev):
    data = bytes(got)

    # Try to carve out the real flag cleanly
    start = data.find(b"0xfun{")
    if start != -1:
        end = data.find(b"}", start)
        if end != -1:
            flag = data[start:end+1]
            print(flag.decode("latin-1", "replace"))
            return

    # fallback: print raw capture if carving fails
    print("RAW:", data)

gdb.events.exited.connect(on_exit)
end

run
```
gdb -q -nx -batch -x extract_flag.gdb --args ./crackme
output:`b'0000xxxxffffuuuunnnn{{{{rrrr3333vvvv____OOOObbbbffffUUUU4444CCCC3333tttt11110000nnnn____mmmm4444SSSStttt3333rrrr____222244446666666644443333666633335555888877776666}}}}'`
each character repeated 4 times so lets clean it using python script
```data = "0000xxxxffffuuuunnnn{{{{rrrr3333vvvv____OOOObbbbffffUUUU4444CCCC3333tttt11110000nnnn____mmmm4444SSSStttt3333rrrr____222244446666666644443333666633335555888877776666}}}}"
flag = data[::4]
print(flag)```

FLAG:`0xfun{r3v_ObfU4C3t10n_m4St3r_246643635876}`

Solved by: ha1qal
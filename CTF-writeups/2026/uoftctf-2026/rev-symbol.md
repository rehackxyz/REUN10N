# rev - Symbol

1. UPX unpack binary
2. Inspect main function
- fgets function takes input and pass to strcspn to count total of 42 characters
- buf will be handled by function f_0 with the variable name of var_78
- based on the challenge name symbol of hope, given clues that symbolic execution can be perform with the tool of angr, with the usage case of stdin and fixed size buffer
3. `nm checker | grep " f_" | wc -l` -> 4200 flag transformation functions 
4. Inspect function f_4200
```c
int64_t f_4200(int64_t arg1)
{
if (memcmp(arg1, &expected, 0x2a))
  return puts("No");        
  return puts("Yes");
}
```
 final validation where memcmp with check against `&expected` at `0x441020`
4. Use angr to solve it by specify constraints, size of bytes for &expected data chunk and flag header
```py
import angr
import claripy
BIN = "./checker"
proj = angr.Project(BIN, auto_load_libs=False)
flag = claripy.BVS("flag", 42 * 8)
state = proj.factory.full_init_state(
    stdin=flag
)
for b in flag.chop(8):
    state.solver.add(b != 0x0a)
    state.solver.add(b != 0x0d)
    state.solver.add(b >= 0x20)
    state.solver.add(b <= 0x7e)
prefix = b"uoftctf{"
for i, c in enumerate(prefix):
    state.solver.add(flag.get_byte(i) == c)
state.solver.add(flag.get_byte(41) == ord('}'))
simgr = proj.factory.simulation_manager(state)
F4200 = 0x440e40
simgr.explore(find=F4200)
assert simgr.found, "Did not reach f_4200"
state = simgr.found[0]
EXPECTED_ADDR = 0x441020
SIZE = 0x2a
buf_ptr = state.regs.rdi
final_buf = state.memory.load(buf_ptr, SIZE)
expected  = state.memory.load(EXPECTED_ADDR, SIZE)
state.solver.add(final_buf == expected)
solution = state.solver.eval(flag, cast_to=bytes)
print("[+] FLAG:", solution)
```
FLAG: `uoftctf{5ymb0l1c_3x3cu710n_15_v3ry_u53ful}`

Solved by: 1337_flagzz
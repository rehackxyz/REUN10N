Inside sub_123E(char *a1), there are 46 successive checks of the form:
- Load a 32-bit constant, reinterpret it as float.
- Call one of the helper routines:
-- sub_1189(double)
-- sub_119D(double)
-- sub_11DC(val, n) / sub_120D(val, n)
- Then apply arithmetic(add/sub/shift/mod).

Reverse by:
- Identify the floating-point constant and compute its numeric value (contoh 0x419CF5C3 → ≈ 19.646 → floor(...) = 19.)
- reverse arithmetic
- repeat with other 45 character

flag: `NHNC{jus7_s0m3_c00l_flo4t1ng_p0in7_0p3ra7ion5}`

Solved by: zeqzoq
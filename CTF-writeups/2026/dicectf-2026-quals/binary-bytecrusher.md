# binary - bytecrusher

Bugs: crush_string() OOB read + gets() overflow
Leak: crush_string
steps input with stride rate. With rate = T (large), the loop jumps from input[0] directly to input[T], skipping the null terminator and landing on raw stack bytes. Leaked value ends up in crushed[1] which puts() prints.

Use 13 of 16 free trials:
rate=73–79 → leak canary bytes 1–7
rate=88–93 → leak return address → PIE base = ret - 0x15ec

Overflow (gets() in get_feedback):
'A'*24 + p64(canary) + 'B'*8 + p64(base + 0x12a9)

→ jumps to admin_portal() which prints flag.txt

Compiled by: yappare
Solved by: Ha1qal
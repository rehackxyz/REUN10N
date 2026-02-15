# misc - not-just-a-hobby

Flag: `lactf{graph1c_d3sign_is_My_PA55i0N!!1!}`

```
import re
import numpy as np
from PIL import Image

PATH = "v.v"
W = H = 128

def parse_num(tok: str):
    tok = tok.strip()
    m = re.fullmatch(r"(\d+)\s*'d\s*(\d+)", tok)
    if m:
        width = int(m.group(1))
        val = int(m.group(2))
        return val % (1 << width), True   # (value, sized?)
    if re.fullmatch(r"\d+", tok):
        return int(tok), False
    raise ValueError(f"Can't parse token: {tok!r}")

text = open(PATH, "r", encoding="utf-8").read()

# Find all (x == ... && y == ...) occurrences
pairs = re.findall(r"\(\s*x\s*==\s*([^&\)]+?)\s*&&\s*y\s*==\s*([^\)]+?)\s*\)", text)

pts = set()
for xs, ys in pairs:
    xv, x_sized = parse_num(xs)
    yv, y_sized = parse_num(ys)

    # Unsized constants must be in 0..127 to ever match 7-bit x/y.
    if (not x_sized and xv > 127) or (not y_sized and yv > 127):
        continue

    if 0 <= xv < W and 0 <= yv < H:
        pts.add((xv, yv))

# Render: white background, black pixels at listed coordinates
img = np.full((H, W), 255, dtype=np.uint8)
for x, y in pts:
    img[y, x] = 0

out = Image.fromarray(img).resize((512, 512), Image.NEAREST)
out.save("out.png")
print("Wrote out.png")
```

Solved by: yappare
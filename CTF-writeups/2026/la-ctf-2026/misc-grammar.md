# misc - grammar

Flag: `lactf{pr0fe55or_p4u1_eggert}`

solver script:

```

```

will print out bunch of potential flags.
the first word looks like professor, googled the CS 131 Programming Languages found Professor Paul Eggert
import cv2
import numpy as np
from itertools import product

IMG_PATH = "tree.png"

# --- chain maps (depth -> char) ---
CON = {1: "f", 2: "g", 3: "p", 4: "t", 5: "r"}
VOW = {1: "e", 2: "o", 3: "u"}
DIG = {1: "0", 2: "1", 3: "4", 4: "5"}

# fragment types -> sequence of categories
# (C/V/D) and arity (len)
FRAGS = {
    "cd": ["C", "D"],
    "vc": ["V", "C"],
    "vd": ["V", "D"],
    "c":  ["C"],
    "d":  ["D"],
}

def decode_char(cat, depth):
    if cat == "C": return CON.get(depth)
    if cat == "V": return VOW.get(depth)
    if cat == "D": return DIG.get(depth)
    return None

def find_terminal_centers(img_gray):
    """
    Terminals are black filled squares at the bottom.
    We detect them by thresholding and contour filtering.
    """
    h, w = img_gray.shape
    roi = img_gray[int(h * 0.85):, :]  # bottom band
    _, bw = cv2.threshold(roi, 60, 255, cv2.THRESH_BINARY_INV)

    cnts, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    centers = []
    for c in cnts:
        x, y, ww, hh = cv2.boundingRect(c)
        area = ww * hh
        # tune these if needed
        if 400 < area < 5000 and abs(ww - hh) < 6:
            cx = x + ww // 2
            cy = int(h * 0.85) + y + hh // 2
            centers.append((cx, cy, ww, hh))
    centers.sort(key=lambda t: t[0])
    return centers

def count_circles_on_stem(img_gray, x, y_top, y_bot, xpad=24):
    """
    Look in a vertical slice above terminal center x.
    Count connected components that look like filled circles.
    """
    h, w = img_gray.shape
    x0 = max(0, x - xpad)
    x1 = min(w, x + xpad)
    y0 = max(0, y_top)
    y1 = min(h, y_bot)

    col = img_gray[y0:y1, x0:x1]
    bw = (col < 80).astype(np.uint8) * 255

    num, labels, stats, centroids = cv2.connectedComponentsWithStats(bw, connectivity=8)
    cnt = 0
    for k in range(1, num):
        area = stats[k, cv2.CC_STAT_AREA]
        ww = stats[k, cv2.CC_STAT_WIDTH]
        hh = stats[k, cv2.CC_STAT_HEIGHT]
        # circles ~ (diameter ~ 30-45px in this image)
        if 250 <= area <= 3000 and 16 <= ww <= 60 and 16 <= hh <= 60:
            # reject long skinny things (lines)
            if ww / hh < 0.55 or ww / hh > 1.8:
                continue
            cnt += 1
    return cnt

def expand_frag_seq(seq):
    cats = []
    for t in seq:
        cats.extend(FRAGS[t])
    return cats

def solve_word(depths, frag_arity_pattern):
    """
    frag_arity_pattern: list where 1 means unary fragment, 2 means binary fragment,
    derived from the colored circles in the tree.
    """
    choices = []
    for a in frag_arity_pattern:
        if a == 1:
            choices.append(["c", "d"])
        else:
            choices.append(["cd", "vc", "vd"])

    sols = []
    for seq in product(*choices):
        cats = expand_frag_seq(seq)
        if len(cats) != len(depths):
            continue
        out = []
        ok = True
        for cat, d in zip(cats, depths):
            ch = decode_char(cat, d)
            if ch is None:
                ok = False
                break
            out.append(ch)
        if ok:
            sols.append(("".join(out), seq))
    return sols

def main():
    img = cv2.imread(IMG_PATH)
    if img is None:
        raise SystemExit("could not read tree.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    terms = find_terminal_centers(gray)
    if len(terms) != 28:
        raise SystemExit(f"expected 28 terminals, found {len(terms)} (adjust thresholds)")

    # count circles above each terminal
    depths = []
    for (cx, cy, ww, hh) in terms:
        # scan from above the boxes upward
        d = count_circles_on_stem(gray, cx, y_top=int(h*0.30), y_bot=int(h*0.88))
        depths.append(d)

    print("depths:", depths)

    # From the tree, fragment arities are:
    # word1: 1,2,1,2,1,2  (ABACDE where B,C,E are binary-looking)
    # word2: 2,2          (BC both binary)
    # word3: 2,1,2,1      (EAEA: E binary, A unary, E binary, A unary)
    #
    # Also start = 6 chars, end = 1 char.
    start = "lactf{"
    end = "}"

    # Find underscores: in this PNG they are the two terminals that have no stem-stack circles
    # inside the middle region (not part of start/end).
    # If your image differs, you can also hardcode them by looking at the tree separators.
    mid = depths[6:-1]  # between start and end
    # heuristic: underscores are the two positions with the smallest circle counts in mid
    idxs = sorted(range(len(mid)), key=lambda i: mid[i])[:2]
    idxs.sort()
    us1 = 6 + idxs[0]
    us2 = 6 + idxs[1]
    print("underscore positions (0-based terminals):", us1, us2)

    w1 = depths[6:us1]
    w2 = depths[us1+1:us2]
    w3 = depths[us2+1:-1]

    # Apply arity patterns from the tree
    s1 = solve_word(w1, [1,2,1,2,1,2])
    s2 = solve_word(w2, [2,2])
    s3 = solve_word(w3, [2,1,2,1])

    print("candidates counts:", len(s1), len(s2), len(s3))

    for a,_ in s1:
        for b,_ in s2:
            for c,_ in s3:
                print(f"{start}{a}_{b}_{c}{end}")

if __name__ == "__main__":
    main()

Solved by: yappare
# rev - flag-finder


Flag :`lactf{Wh47_d0_y0u_637_wh3n_y0u_cr055_4_r363x_4nd_4_n0n06r4m?_4_r363x06r4m!}`
https://cdn.discordapp.com/attachments/1469958535092899873/1469958879549849722/image.png?ex=69921f23&is=6990cda3&hm=e5bc9c1d5e5182455b7ea890d821d3ffd9f7caa5f460b13332a682fe862709de&
```
#!/usr/bin/env python3
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

ROWS, COLS = 19, 101


def load_js_regex_from_script(path: str = "script.js") -> str:
    js = Path(path).read_text("utf-8")
    m = re.search(r"const theFlag = /(.*?)/;\s*$", js, re.S | re.M)
    if not m:
        raise SystemExit("Could not extract `const theFlag = /.../;` from script.js")
    return m.group(1)


def extract_top_level_lookaheads(rx: str):
    if not rx.startswith("^"):
        raise ValueError("regex does not start with '^'")
    i = 1
    out = []
    while i < len(rx) and rx.startswith("(?=", i):
        i += 3
        start = i
        depth = 1
        while i < len(rx) and depth > 0:
            ch = rx[i]
            if ch == "\\":
                i += 2
                continue
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            i += 1
        out.append(rx[start : i - 1])
    return out


def extract_lookaheads_at_this_level(text: str):
    out = []
    i = 0
    while i < len(text):
        if text.startswith("(?=", i):
            i += 3
            start = i
            depth = 1
            while i < len(text) and depth > 0:
                ch = text[i]
                if ch == "\\":
                    i += 2
                    continue
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                i += 1
            out.append(text[start : i - 1])
        else:
            i += 1
    return out


# Unit describing a single row contribution for a fixed column c inside the wrapper lookaheads.
# Examples:
#   (?:.{52}\..{48})  -> column 52 is '.' for that row
#   (?:.{91}#.{9})    -> column 91 is '#'
#   (?:.{99}#.)       -> column 99 is '#', tail==1 compact
#   (?:.{100}\.)      -> column 100 is '.', tail==0 compact
UNIT_RE = re.compile(
    r"\(\?:"
    r"(?:(?:\.\{(?P<pn>\d+)\})|(?P<p1>\.))?"
    r"(?P<mark>#|\\\.)"
    r"(?:(?:\.\{(?P<sn>\d+)\})|(?P<s1>\.))?"
    r"\)"
)


def unit_lengths(m: re.Match):
    pref = int(m.group("pn")) if m.group("pn") is not None else (1 if m.group("p1") else 0)
    suff = int(m.group("sn")) if m.group("sn") is not None else (1 if m.group("s1") else 0)
    return pref, suff, m.group("mark")


def infer_col_from_lookahead(la: str) -> int:
    for m in UNIT_RE.finditer(la):
        pref, suff, _ = unit_lengths(m)
        if pref + 1 + suff == COLS:
            return pref
    raise ValueError("could not infer column from lookahead: " + la[:80])


def lookahead_to_col_regex_digits(la: str, col: int) -> str:
    # Replace each per-row unit for this column with a digit:
    # '\.' -> '0', '#' -> '1'
    def repl(m: re.Match):
        pref, suff, mark = unit_lengths(m)
        if pref + 1 + suff != COLS or pref != col:
            return m.group(0)
        return "1" if mark == "#" else "0"

    out = UNIT_RE.sub(repl, la)
    if "(?:" in out or r"\." in out or re.search(r"\.\{\d+\}", out) or "#" in out:
        raise ValueError(f"unexpected leftovers in column regex for col={col}: {out[:160]}")
    return out


def parse_digit_run_regex(rx: str):
    # Tokenize a run-only regex like: 0*1{4}0+1{2}0*
    tokens = []
    i = 0
    while i < len(rx):
        ch = rx[i]
        if ch in "()?:":
            i += 1
            continue
        if ch not in "01":
            raise ValueError(f"unexpected char in digit regex: {ch!r} in {rx[:120]}")
        i += 1
        if i < len(rx) and rx[i] in "*+":
            q = rx[i]
            i += 1
            mn = 0 if q == "*" else 1
            mx = ROWS  # bounded by total length
        elif i < len(rx) and rx[i] == "{":
            j = rx.find("}", i)
            if j < 0:
                raise ValueError("unterminated {n} in: " + rx[:120])
            n = int(rx[i + 1 : j])
            i = j + 1
            mn = mx = n
        else:
            mn = mx = 1
        tokens.append((ch, mn, mx))
    return tokens


def extract_row_fragments(rx: str):
    row_re = re.compile(
        r"\(\?<=\.\{(\d+)\}\)\(\?<!\.\{(\d+)\}\)\((.*?)\)"
        r"(?=\(\?<=\.\{\d+\}\)\(\?<!\.\{\d+\}\)|\(\?<=\.\{1919\}\)|\$\Z|\$)",
        re.S,
    )
    frags = [m.group(3) for m in row_re.finditer(rx)]
    frags = [r"\.*"] + frags  # group1: (\.*)
    if len(frags) != ROWS:
        raise ValueError(f"expected {ROWS} row fragments, got {len(frags)}")
    return frags


def row_frag_to_blocks(frag: str):
    # Extract the hash-run lengths: '#', '#{n}'
    blocks = []
    i = 0
    while i < len(frag):
        if frag.startswith("#{", i):
            j = frag.find("}", i)
            blocks.append(int(frag[i + 2 : j]))
            i = j + 1
        elif frag[i] == "#":
            blocks.append(1)
            i += 1
        else:
            i += 1
    return blocks


@dataclass(frozen=True)
class Automaton:
    # Deterministic automaton for standard nonogram clues:
    # blocks are 1-runs separated by >=1 zeros, with optional leading/trailing zeros.
    next0: tuple  # next state on 0 (or -1)
    next1: tuple  # next state on 1 (or -1)
    start: int
    accept: int


@lru_cache(maxsize=None)
def build_automaton(blocks: tuple[int, ...]) -> Automaton:
    k = len(blocks)

    # State space:
    # GF(i): gap free, next block index i (0..k)
    # GN(i): gap needed, must place a 0 before starting block i (1..k-1)
    # IN(i, rem): inside block i, need rem more 1s to finish (1..blocks[i]-1)
    states = []
    idx = {}

    def add(state):
        if state not in idx:
            idx[state] = len(states)
            states.append(state)

    for i in range(k + 1):
        add(("GF", i, 0))
    for i in range(1, k):
        add(("GN", i, 0))
    for i, blen in enumerate(blocks):
        for rem in range(1, blen):
            add(("IN", i, rem))

    n = len(states)
    next0 = [-1] * n
    next1 = [-1] * n

    def get(state):
        return idx[state]

    for s_i, s in enumerate(states):
        kind, i, rem = s
        if kind == "GF":
            # 0: stay in gap
            next0[s_i] = get(("GF", i, 0))
            # 1: start block i if any remain
            if i < k:
                blen = blocks[i]
                if blen == 1:
                    # finish immediately
                    if i == k - 1:
                        next1[s_i] = get(("GF", k, 0))
                    else:
                        next1[s_i] = get(("GN", i + 1, 0))
                else:
                    next1[s_i] = get(("IN", i, blen - 1))
        elif kind == "GN":
            # must place 0, then gap free
            next0[s_i] = get(("GF", i, 0))
            next1[s_i] = -1
        else:  # IN
            # must place 1
            if rem > 1:
                next1[s_i] = get(("IN", i, rem - 1))
            else:
                # finish block i
                if i == k - 1:
                    next1[s_i] = get(("GF", k, 0))
                else:
                    next1[s_i] = get(("GN", i + 1, 0))
            next0[s_i] = -1

    start = get(("GF", 0, 0))
    accept = get(("GF", k, 0))
    return Automaton(tuple(next0), tuple(next1), start, accept)


def line_deduce(blocks: list[int], L: int, known1: int, known0: int):
    # Return (forced1_mask, forced0_mask) for this line, or None if impossible.
    if known1 & known0:
        return None

    a = build_automaton(tuple(blocks))
    n = len(a.next0)

    def allowed0(pos: int) -> bool:
        return ((known1 >> pos) & 1) == 0

    def allowed1(pos: int) -> bool:
        return ((known0 >> pos) & 1) == 0

    # Forward reachable state sets (bitsets).
    F = [0] * (L + 1)
    F[0] = 1 << a.start
    for p in range(L):
        cur = F[p]
        nxt = 0
        if cur == 0:
            break
        a0 = allowed0(p)
        a1 = allowed1(p)
        # iterate states (n is small)
        for s in range(n):
            if (cur >> s) & 1:
                if a0:
                    t = a.next0[s]
                    if t != -1:
                        nxt |= 1 << t
                if a1:
                    t = a.next1[s]
                    if t != -1:
                        nxt |= 1 << t
        F[p + 1] = nxt

    if ((F[L] >> a.accept) & 1) == 0:
        return None

    # Backward: states that can reach accept from position p.
    B = [0] * (L + 1)
    B[L] = 1 << a.accept
    for p in range(L - 1, -1, -1):
        nxt = B[p + 1]
        cur = 0
        a0 = allowed0(p)
        a1 = allowed1(p)
        for s in range(n):
            if a0:
                t = a.next0[s]
                if t != -1 and ((nxt >> t) & 1):
                    cur |= 1 << s
                    continue
            if a1:
                t = a.next1[s]
                if t != -1 and ((nxt >> t) & 1):
                    cur |= 1 << s
        B[p] = cur

    forced1 = 0
    forced0 = 0
    for p in range(L):
        a0 = allowed0(p)
        a1 = allowed1(p)
        pre = F[p]
        suf = B[p + 1]

        can0 = False
        can1 = False
        if pre:
            for s in range(n):
                if ((pre >> s) & 1) == 0:
                    continue
                if a0 and not can0:
                    t = a.next0[s]
                    if t != -1 and ((suf >> t) & 1):
                        can0 = True
                if a1 and not can1:
                    t = a.next1[s]
                    if t != -1 and ((suf >> t) & 1):
                        can1 = True
                if can0 and can1:
                    break

        if not can0 and not can1:
            return None
        if can1 and not can0:
            forced1 |= 1 << p
        elif can0 and not can1:
            forced0 |= 1 << p

    return forced1, forced0


def line_count(blocks: list[int], L: int, known1: int, known0: int, cap: int = 10**9) -> int:
    # Count number of solutions for heuristic (only used for L==ROWS, small).
    if known1 & known0:
        return 0
    a = build_automaton(tuple(blocks))
    n = len(a.next0)
    dp = [0] * n
    dp[a.start] = 1
    for p in range(L):
        ndp = [0] * n
        a0 = ((known1 >> p) & 1) == 0
        a1 = ((known0 >> p) & 1) == 0
        for s in range(n):
            v = dp[s]
            if not v:
                continue
            if a0:
                t = a.next0[s]
                if t != -1:
                    ndp[t] = min(cap, ndp[t] + v)
            if a1:
                t = a.next1[s]
                if t != -1:
                    ndp[t] = min(cap, ndp[t] + v)
        dp = ndp
    return dp[a.accept]


@dataclass
class Grid:
    row1: list[int]  # 1 bits by row (len ROWS)
    row0: list[int]  # 0 bits by row
    col1: list[int]  # 1 bits by col (len COLS, bits over rows)
    col0: list[int]  # 0 bits by col

    def clone(self) -> "Grid":
        return Grid(self.row1[:], self.row0[:], self.col1[:], self.col0[:])

    def is_solved(self) -> bool:
        full = (1 << COLS) - 1
        return all(((self.row1[r] | self.row0[r]) == full) for r in range(ROWS))

    def set_cell(self, r: int, c: int, v: int) -> bool:
        bc = 1 << c
        br = 1 << r
        if v == 1:
            if self.row0[r] & bc:
                return False
            if self.row1[r] & bc:
                return True
            self.row1[r] |= bc
            self.col1[c] |= br
            self.row0[r] &= ~bc
            self.col0[c] &= ~br
            return True
        else:
            if self.row1[r] & bc:
                return False
            if self.row0[r] & bc:
                return True
            self.row0[r] |= bc
            self.col0[c] |= br
            self.row1[r] &= ~bc
            self.col1[c] &= ~br
            return True


def propagate(g: Grid, row_blocks: list[list[int]], col_blocks: list[list[int]]) -> bool:
    full_row_mask = (1 << COLS) - 1
    changed = True
    while changed:
        changed = False

        # Rows
        for r in range(ROWS):
            res = line_deduce(row_blocks[r], COLS, g.row1[r], g.row0[r])
            if res is None:
                return False
            f1, f0 = res
            new1 = f1 & ~(g.row1[r] | g.row0[r])
            new0 = f0 & ~(g.row1[r] | g.row0[r])
            if new1 or new0:
                changed = True
            while new1:
                b = new1 & -new1
                c = (b.bit_length() - 1)
                if not g.set_cell(r, c, 1):
                    return False
                new1 &= new1 - 1
            while new0:
                b = new0 & -new0
                c = (b.bit_length() - 1)
                if not g.set_cell(r, c, 0):
                    return False
                new0 &= new0 - 1

        # Columns
        for c in range(COLS):
            res = line_deduce(col_blocks[c], ROWS, g.col1[c], g.col0[c])
            if res is None:
                return False
            f1, f0 = res
            known = g.col1[c] | g.col0[c]
            new1 = f1 & ~known
            new0 = f0 & ~known
            if new1 or new0:
                changed = True
            while new1:
                b = new1 & -new1
                r = (b.bit_length() - 1)
                if not g.set_cell(r, c, 1):
                    return False
                new1 &= new1 - 1
            while new0:
                b = new0 & -new0
                r = (b.bit_length() - 1)
                if not g.set_cell(r, c, 0):
                    return False
                new0 &= new0 - 1

        # Quick consistency: no row may have conflicting knowns.
        for r in range(ROWS):
            if g.row1[r] & g.row0[r]:
                return False
            if (g.row1[r] | g.row0[r]) & ~full_row_mask:
                return False

    return True


def search(g: Grid, row_blocks: list[list[int]], col_blocks: list[list[int]]) -> Grid | None:
    if not propagate(g, row_blocks, col_blocks):
        return None
    if g.is_solved():
        return g

    # Heuristic: pick the most constrained column (fewest solutions) that still has unknowns.
    best_c = None
    best_count = None
    for c in range(COLS):
        if (g.col1[c] | g.col0[c]) == (1 << ROWS) - 1:
            continue
        cnt = line_count(col_blocks[c], ROWS, g.col1[c], g.col0[c], cap=10**7)
        if cnt <= 1:
            continue
        if best_count is None or cnt < best_count:
            best_count = cnt
            best_c = c
            if cnt == 2:
                break

    if best_c is None:
        # Fallback: first unknown cell
        for r in range(ROWS):
            unk = ~ (g.row1[r] | g.row0[r]) & ((1 << COLS) - 1)
            if unk:
                c = (unk & -unk).bit_length() - 1
                best_c = c
                break

    c = best_c
    # Choose an unknown row in that column.
    unk_rows = ~ (g.col1[c] | g.col0[c]) & ((1 << ROWS) - 1)
    r = (unk_rows & -unk_rows).bit_length() - 1

    # Try 1 then 0.
    g1 = g.clone()
    if g1.set_cell(r, c, 1):
        res = search(g1, row_blocks, col_blocks)
        if res is not None:
            return res
    g0 = g.clone()
    if g0.set_cell(r, c, 0):
        res = search(g0, row_blocks, col_blocks)
        if res is not None:
            return res
    return None


def main():
    rx = load_js_regex_from_script("script.js")

    # Row clues from the tail of the big regex.
    row_frags = extract_row_fragments(rx)
    row_blocks = [row_frag_to_blocks(f) for f in row_frags]

    # Column clues from the wrapper lookaheads.
    wrapper = extract_top_level_lookaheads(rx)[0]
    lookaheads = extract_lookaheads_at_this_level(wrapper)
    if len(lookaheads) != COLS:
        raise SystemExit(f"Expected {COLS} column lookaheads, got {len(lookaheads)}")

    col_blocks = [None] * COLS
    for la in lookaheads:
        c = infer_col_from_lookahead(la)
        if col_blocks[c] is not None:
            raise SystemExit(f"duplicate constraints for column {c}")
        digit_rx = lookahead_to_col_regex_digits(la, c)
        toks = parse_digit_run_regex(digit_rx)
        blocks = []
        for ch, mn, mx in toks:
            if ch == "1":
                if mn != mx:
                    raise SystemExit(f"variable 1-run in column {c}: {digit_rx[:80]}")
                if mn > 0:
                    blocks.append(mn)
        col_blocks[c] = blocks

    if any(v is None for v in col_blocks):
        missing = [i for i, v in enumerate(col_blocks) if v is None]
        raise SystemExit(f"missing columns: {missing}")

    g = Grid(row1=[0] * ROWS, row0=[0] * ROWS, col1=[0] * COLS, col0=[0] * COLS)
    solved = search(g, row_blocks, col_blocks)
    if solved is None:
        raise SystemExit("No solution found")

    print("=== GRID (19x101) ===")
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append("#" if (solved.row1[r] >> c) & 1 else ".")
        print("".join(row))


if __name__ == "__
```
Solved by: Zeqzoq

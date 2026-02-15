# crypto - not-so-lazy-trigrams

Flag: `lactf{still_too_lazy_to_write_a_plaintext_so_heres_a_random_wikipedia_article}`

```

```
#!/usr/bin/env python3
import math
import random
import re
import sys
from collections import Counter, defaultdict

# ---------------------------
# 1) Read ciphertext
# ---------------------------
def read_ct(path="ct.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# ---------------------------
# 2) This cipher is separable:
#    ciphertext letters at positions mod 3 each undergo their own substitution.
#    (Because sub_trigrams is a cartesian product of three shuffled alphabets.)
# ---------------------------

ALPH = "abcdefghijklmnopqrstuvwxyz"
A2I = {c:i for i,c in enumerate(ALPH)}
I2A = {i:c for i,c in enumerate(ALPH)}

def only_letters(s: str) -> str:
    return re.sub(r"[^a-zA-Z]", "", s).lower()

def apply_decrypt_full(ct: str, inv_maps, offset_mod3: int) -> str:
    """
    inv_maps: list of 3 lists length 26 mapping cipher_index -> plain_index
    offset_mod3: how to align the first alphabetic character in ct to stream position 0
                (0 means first alpha is class 0, next is class 1, etc.)
    """
    out = []
    k = 0  # counts alpha chars
    for ch in ct:
        if ch.isalpha():
            c = ch.lower()
            ci = A2I[c]
            cls = (k + offset_mod3) % 3
            pi = inv_maps[cls][ci]
            out.append(I2A[pi])
            k += 1
        else:
            out.append(ch)
    return "".join(out)

def decrypt_alpha_stream(alpha: str, inv_maps, offset_mod3: int) -> str:
    """
    alpha: letters-only ciphertext stream.
    """
    res = []
    for k, c in enumerate(alpha):
        ci = A2I[c]
        cls = (k + offset_mod3) % 3
        pi = inv_maps[cls][ci]
        res.append(I2A[pi])
    return "".join(res)

# ---------------------------
# 3) Tetragram scoring
# ---------------------------

# If you have a real quadgram frequency file (PracticalCryptography style),
# put it in the same folder as english_quadgrams.txt:
# Each line: "THEN 12345"
# But since we can't assume that, we fall back to building from an embedded corpus.
def load_quadgrams(path="english_quadgrams.txt"):
    try:
        quad = {}
        total = 0
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 2:
                    continue
                g, n = parts[0].lower(), int(parts[1])
                quad[g] = n
                total += n
        if total > 0:
            return quad, total
    except FileNotFoundError:
        pass
    return None, None

EMBED_CORPUS = r"""
alice was beginning to get very tired of sitting by her sister on the bank and of having nothing to do
once or twice she had peeped into the book her sister was reading but it had no pictures or conversations
in it and what is the use of a book thought alice without pictures or conversations
so she was considering in her own mind as well as she could for the hot day made her feel very sleepy and stupid
whether the pleasure of making a daisy chain would be worth the trouble of getting up and picking the daisies
when suddenly a white rabbit with pink eyes ran close by her
there was nothing so very remarkable in that nor did alice think it so very much out of the way to hear the rabbit say to itself
oh dear oh dear i shall be late
when she thought it over afterwards it occurred to her that she ought to have wondered at this but at the time it all seemed quite natural
but when the rabbit actually took a watch out of its waistcoat pocket and looked at it and then hurried on
alice started to her feet for it flashed across her mind that she had never before seen a rabbit with either a waistcoat pocket
or a watch to take out of it and burning with curiosity she ran across the field after it
"""

def build_quadgrams_from_corpus(text: str):
    text = re.sub(r"[^a-zA-Z]", "", text).lower()
    quad = Counter()
    for i in range(len(text) - 3):
        quad[text[i:i+4]] += 1
    total = sum(quad.values())
    return dict(quad), total

def make_quad_scorer():
    quad, total = load_quadgrams()
    if quad is None:
        quad, total = build_quadgrams_from_corpus(EMBED_CORPUS)

    # Convert to log probabilities with add-one-ish smoothing
    # Unknown grams get floor probability.
    floor = math.log10(0.01 / total)
    logp = {}
    for g, n in quad.items():
        logp[g] = math.log10(n / total)
    return logp, floor

LOGQ, FLOORQ = make_quad_scorer()

def score_text_quadgrams(text: str) -> float:
    text = re.sub(r"[^a-zA-Z]", "", text).lower()
    if len(text) < 4:
        return -1e18
    s = 0.0
    for i in range(len(text) - 3):
        g = text[i:i+4]
        s += LOGQ.get(g, FLOORQ)
    return s

# ---------------------------
# 4) Simulated annealing / hillclimb over 3 inverse permutations
# ---------------------------

def random_perm():
    p = list(range(26))
    random.shuffle(p)
    return p

def invert_perm(enc_map_plain_to_cipher):
    inv = [0]*26
    for p, c in enumerate(enc_map_plain_to_cipher):
        inv[c] = p
    return inv

def perm_as_str(inv_map):
    # cipher->plain mapping shown as letters
    return "".join(I2A[inv_map[i]] for i in range(26))

def swap_two(p):
    a = random.randrange(26)
    b = random.randrange(26)
    if a == b:
        b = (b + 1) % 26
    p2 = p[:]
    p2[a], p2[b] = p2[b], p2[a]
    return p2

def anneal(alpha_ct: str, offset_mod3: int, iters=200000, start_temp=5.0, end_temp=0.2):
    """
    Optimize inv_maps (3 inverse substitutions) for a given offset_mod3.
    """
    # inv_maps[cls][cipher_index] = plain_index
    inv_maps = [random_perm(), random_perm(), random_perm()]

    best_maps = [m[:] for m in inv_maps]
    best_plain = decrypt_alpha_stream(alpha_ct, best_maps, offset_mod3)
    best_score = score_text_quadgrams(best_plain)

    cur_maps = [m[:] for m in inv_maps]
    cur_plain = best_plain
    cur_score = best_score

    # annealing schedule
    for t in range(1, iters + 1):
        frac = t / iters
        temp = start_temp * (1 - frac) + end_temp * frac

        # pick which class to mutate
        cls = random.randrange(3)
        trial_maps = [m[:] for m in cur_maps]
        trial_maps[cls] = swap_two(trial_maps[cls])

        trial_plain = decrypt_alpha_stream(alpha_ct, trial_maps, offset_mod3)
        trial_score = score_text_quadgrams(trial_plain)

        delta = trial_score - cur_score
        if delta >= 0 or random.random() < math.exp(delta / max(temp, 1e-9)):
            cur_maps = trial_maps
            cur_plain = trial_plain
            cur_score = trial_score

            if cur_score > best_score:
                best_score = cur_score
                best_maps = [m[:] for m in cur_maps]

        # occasional progress
        if t % (iters // 10 or 1) == 0:
            print(f"    iter {t}/{iters} score={best_score:.2f}", flush=True)

    return best_maps, best_score

def multi_restart(alpha_ct: str, offset_mod3: int, restarts=8, iters=200000):
    best = None
    best_score = -1e18
    for r in range(restarts):
        print(f"  [*] restart {r+1}/{restarts} (offset={offset_mod3})")
        maps, sc = anneal(alpha_ct, offset_mod3, iters=iters)
        if sc > best_score:
            best_score = sc
            best = maps
            print(f"  [+] new best for offset={offset_mod3}: {best_score:.2f}")
    return best, best_score

# ---------------------------
# 5) Extract flag
# ---------------------------
FLAG_RE = re.compile(r"lactf\{[^\}]+\}")

def find_flag_in_text(s: str):
    m = FLAG_RE.search(s)
    return m.group(0) if m else None

# ---------------------------
# Main
# ---------------------------
def main():
    random.seed(0xC0FFEE)

    ct = read_ct("ct.txt")
    alpha_ct = only_letters(ct)

    # Tuning knobs:
    ITERS = 250000     # per restart
    RESTARTS = 10      # per offset
    # If it runs too slow: reduce ITERS/RESTARTS.
    # If it doesn't converge: increase them.

    overall_best = None
    overall_best_score = -1e18
    overall_best_offset = None

    # Try all 3 possible offsets (because we don't know alignment mod 3)
    for offset in (0, 1, 2):
        print(f"[+] Solving with offset_mod3 = {offset}")
        maps, sc = multi_restart(alpha_ct, offset, restarts=RESTARTS, iters=ITERS)
        print(f"[+] Best score offset {offset}: {sc:.2f}")
        if sc > overall_best_score:
            overall_best_score = sc
            overall_best = maps
            overall_best_offset = offset

        # quick check for flag after each offset
        dec_full = apply_decrypt_full(ct, maps, offset)
        flag = find_flag_in_text(dec_full)
        if flag:
            print("\n[!] FLAG FOUND:", flag)
            return

    print("\n[+] Best overall offset:", overall_best_offset, "score:", overall_best_score)

    dec_full = apply_decrypt_full(ct, overall_best, overall_best_offset)
    flag = find_flag_in_text(dec_full)
    if flag:
        print("\n[!] FLAG FOUND:", flag)
    else:
        print("\n[-] No lactf{...} found yet.")
        print("    Try increasing ITERS/RESTARTS, or provide a real english_quadgrams.txt for better scoring.")
        # show a snippet around where the ciphertext currently has braces to help manual spotting
        brace_i = dec_full.find("{")
        if brace_i != -1:
            print("\n[debug] snippet near first '{':")
            print(dec_full[max(0, brace_i-80): brace_i+200])

if __name__ == "__main__":
    main()

Solved by: yappare
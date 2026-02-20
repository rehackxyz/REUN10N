# hardware - Analog Nostalgia

`python3 solve_vga.py signal.bin --ocr -o frame.png`

FLAG:`0XFUN{AN4LOG_IS_NOT_D3AD_JUST_BL4NKING}`
```python
#!/usr/bin/env python3
import argparse
import io
import re
import zipfile

import numpy as np
from PIL import Image, ImageOps, ImageFilter


def split_signal_file(path: str):
    """
    signal.bin layout (for this challenge):
      - ASCII header line ending with \n
      - raw samples: (R,G,B,HS,VS) bytes repeated at pixel-clock rate
      - optional ZIP trailer (starts with PK\x03\x04) containing hint(s)
    """
    data = open(path, "rb").read()

    # Strip header line if present
    nl = data.find(b"\n")
    body = data[nl + 1 :] if nl != -1 else data

    trailer = {}
    # If there's a ZIP appended, peel it off.
    zstart = body.rfind(b"PK\x03\x04")
    if zstart != -1:
        try:
            zf = zipfile.ZipFile(io.BytesIO(body[zstart:]))
            trailer = {name: zf.read(name) for name in zf.namelist()}
            body = body[:zstart]
        except zipfile.BadZipFile:
            pass

    return body, trailer


def decode_frame(payload: bytes) -> Image.Image:
    if len(payload) % 5 != 0:
        raise ValueError(f"payload size {len(payload)} is not divisible by 5 (R,G,B,HS,VS).")

    samples = np.frombuffer(payload, dtype=np.uint8).reshape(-1, 5)
    n = samples.shape[0]

    # Standard 640x480@60 timings -> 800x525 total pixel clocks per frame.
    W, H = 800, 525
    if n != W * H:
        raise ValueError(f"unexpected sample count {n}, expected {W*H} (800*525).")

    frame = samples.reshape(H, W, 5)

    # First 3 channels are 6-bit-ish (0..63). Scale to 8-bit.
    rgb6 = frame[:, :, :3].astype(np.float32)
    rgb8 = np.clip(rgb6 * (255.0 / 63.0), 0, 255).astype(np.uint8)

    # In this capture the active picture is already aligned at the top-left.
    active = rgb8[:480, :640, :]
    im = Image.fromarray(active)
    # Contrast boost so text is readable
    im = ImageOps.autocontrast(im)
    return im


def normalize_underscores(s: str) -> str:
    s = re.sub(r"_+", "_", s)
    return s.strip("_")


def ocr_flag(im: Image.Image):
    """
    Best-effort OCR of the bottom caption.
    If it fails, just open the saved PNG and read it (flag is the bottom text).
    """
    try:
        import pytesseract
    except ImportError:
        return None, "pytesseract not installed"

    # Bottom caption region (tuned for this capture)
    bottom = im.crop((0, 340, im.width, im.height))
    bottom = bottom.resize((bottom.width * 4, bottom.height * 4), Image.Resampling.LANCZOS)

    g = ImageOps.autocontrast(bottom.convert("L"))
    g = g.filter(ImageFilter.UnsharpMask(radius=2, percent=200, threshold=3))

    raw = pytesseract.image_to_string(g, config="--oem 1 --psm 6")

    # Turn into a single token-ish string
    s = raw.strip().upper()
    s = s.replace(" ", "_").replace("\\", "_")
    s = s.replace("(", "{").replace(")", "}")

    # Keep only likely charset
    s = re.sub(r"[^0-9A-Z{}_X]", "", s)

    # Normalize prefix (OCR often turns 0 -> O)
    s = s.replace("OXFUN", "0XFUN")

    m = re.search(r"0XFUN\{[0-9A-Z_]+\}", s)
    if not m:
        return None, raw.strip()

    inside = m.group(0)[len("0XFUN{"):-1]

    # Light heuristic fixes for common OCR confusions in this image
    inside = inside.replace("ANGLOG", "AN4LOG").replace("ANALOG", "AN4LOG")
    inside = inside.replace("DSAD", "D3AD")
    inside = inside.replace("BLANKING", "BL4NKING")

    # Insert missing underscores if they got dropped
    inside = inside.replace("AN4LOGIS", "AN4LOG_IS")
    inside = inside.replace("ISNOT", "IS_NOT")
    inside = inside.replace("NOTD3AD", "NOT_D3AD")
    inside = inside.replace("D3ADJUST", "D3AD_JUST")
    inside = inside.replace("JUSTBL4NKING", "JUST_BL4NKING")
    inside = normalize_underscores(inside)

    flag = "0xFUN{" + inside + "}"
    return flag, raw.strip()


def main():
    ap = argparse.ArgumentParser(description="Decode a single 640x480 VGA frame from signal.bin")
    ap.add_argument("signal", help="path to signal.bin")
    ap.add_argument("-o", "--out", default="frame.png", help="output PNG path (default: frame.png)")
    ap.add_argument("--ocr", action="store_true", help="try OCR to print the flag too")
    args = ap.parse_args()

    payload, trailer = split_signal_file(args.signal)
    im = decode_frame(payload)
    im.save(args.out)
    print(f"[+] wrote {args.out}")

    if trailer:
        print("[+] trailer files:")
        for k, v in trailer.items():
            try:
                print(f"    {k}: {v.decode('utf-8', 'replace').strip()}")
            except Exception:
                print(f"    {k}: <{len(v)} bytes>")

    if args.ocr:
        flag, debug = ocr_flag(im)
        if flag:
            print(f"[+] flag: {flag}")
        else:
            print("[!] OCR didn't confidently extract the flag.")
            print("[!] OCR output was:")
            print(debug)
            print("[!] Open the PNG and read the bottom caption manually.")


if __name__ == "__main__":

    main()
```
Solved by: ha1qal

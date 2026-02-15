# misc - keep scripting


SOLVED by Jigenz
```
import socket
import select
import re
import ast
import time
import sys

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
MODULE_RE = re.compile(r"Module: ([^\n\r]+)")
DATA_RE = re.compile(r"Data: (\{.*?\})")
RE_AMOUNT = re.compile(r"'amount': (\\d+)")
RE_COLORS = re.compile(r"'colors': \\[(.*?)\\]")
RE_SYMBOLS = re.compile(r"'symbols': \\[(.*?)\\]")
RE_LEDS = re.compile(r"'leds': \\[(.*?)\\]")
RE_STARS = re.compile(r"'stars': \\[(.*?)\\]")
RE_COLOR = re.compile(r"'color': '([^']+)'")
RE_TEXT = re.compile(r"'text': '([^']+)'")
RE_STRIP = re.compile(r"'color_strip': '([^']+)'")

KEYPAD_COLUMNS = [
    # column 1
    [0x03D8, 0x0466, 0x019B, 0x03DE, 0x046C, 0x03D7, 0x03FF],
    # column 2
    [0x04EC, 0x03D8, 0x03FF, 0x04A8, 0x2606, 0x03D7, 0x00BF],
    # column 3
    [0x00A9, 0x047C, 0x04A8, 0x0496, 0x0506, 0x019B, 0x2606],
    # column 4
    [0x0431, 0x00B6, 0x048A, 0x046C, 0x0496, 0x00BF, 0x067C],
    # column 5
    [0x03C8, 0x067C, 0x048A, 0x03FE, 0x00B6, 0x046E, 0x2605],
    # column 6
    [0x0431, 0x04EC, 0x0482, 0x00E6, 0x03C8, 0x048A, 0x03A9],
]

COMPLICATED_TABLE = {
    # key: (red, blue, star, led)
    (0, 0, 0, 0): "C",
    (0, 0, 0, 1): "D",
    (0, 0, 1, 0): "C",
    (0, 0, 1, 1): "B",
    (0, 1, 0, 0): "S",
    (0, 1, 0, 1): "P",
    (0, 1, 1, 0): "D",
    (0, 1, 1, 1): "P",
    (1, 0, 0, 0): "S",
    (1, 0, 0, 1): "B",
    (1, 0, 1, 0): "C",
    (1, 0, 1, 1): "B",
    (1, 1, 0, 0): "S",
    (1, 1, 0, 1): "S",
    (1, 1, 1, 0): "P",
    (1, 1, 1, 1): "D",
}


def read_some(sock, timeout=0.1):
    rlist, _, _ = select.select([sock], [], [], timeout)
    if not rlist:
        return b""
    return sock.recv(4096)


def read_until(sock, patterns, timeout=0.6):
    if isinstance(patterns, (bytes, bytearray)):
        patterns = [patterns]
    end = time.time() + timeout
    data = b""
    while time.time() < end:
        remaining = end - time.time()
        if remaining <= 0:
            break
        rlist, _, _ = select.select([sock], [], [], remaining)
        if not rlist:
            break
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
        for p in patterns:
            if p in data:
                return data
    return data


def read_until_text(sock, pattern, timeout=1.2):
    end = time.time() + timeout
    data = b""
    while time.time() < end:
        chunk = read_some(sock, timeout=0.1)
        if not chunk:
            continue
        data += chunk
        if pattern in data:
            break
    return data


def clean_text(data):
    text = data.decode("utf-8", errors="ignore")
    return ANSI_RE.sub("", text)


def parse_header(text):
    serial_m = re.search(r"Serial Number: (\d+)", text)
    batteries_m = re.search(r"Batteries: (\d+)", text)
    label_m = re.search(r"Label: ([A-Z]+)", text)
    ports_m = re.search(r"Ports: ([^\n\r]+)", text)
    serial = serial_m.group(1) if serial_m else ""
    batteries = int(batteries_m.group(1)) if batteries_m else 0
    label = label_m.group(1) if label_m else ""
    ports = []
    if ports_m:
        ports = [p.strip().lower() for p in ports_m.group(1).split(",")]
    return {
        "serial": serial,
        "last_digit": int(serial[-1]) if serial else 0,
        "batteries": batteries,
        "label": label,
        "ports": ports,
    }


def solve_wires(data, bomb):
    colors = data["colors"]
    count = {c: colors.count(c) for c in set(colors)}
    last = colors[-1]
    last_digit_odd = bomb["last_digit"] % 2 == 1

    if data["amount"] == 3:
        if count.get("Red", 0) == 0:
            return 2
        if last == "White":
            return 3
        if count.get("Blue", 0) > 1:
            return len(colors) - 1 - list(reversed(colors)).index("Blue") + 1
        return 3

    if data["amount"] == 4:
        if count.get("Red", 0) > 1 and last_digit_odd:
            return len(colors) - list(reversed(colors)).index("Red")
        if last == "Yellow" and count.get("Red", 0) == 0:
            return 1
        if count.get("Blue", 0) == 1:
            return 1
        if count.get("Yellow", 0) > 1:
            return len(colors)
        return 2

    if data["amount"] == 5:
        if last == "Black" and last_digit_odd:
            return 4
        if count.get("Red", 0) == 1 and count.get("Yellow", 0) > 1:
            return 1
        if count.get("Black", 0) == 0:
            return 2
        return 1

    if data["amount"] == 6:
        if count.get("Yellow", 0) == 0 and last_digit_odd:
            return 3
        if count.get("Yellow", 0) == 1 and count.get("White", 0) > 1:
            return 4
        if count.get("Red", 0) == 0:
            return 6
        return 4

    raise ValueError("Unexpected wires amount")


def solve_button(data, bomb):
    color = data["color"]
    text = data["text"]
    strip = data["color_strip"]
    batteries = bomb["batteries"]
    label = bomb["label"]

    def strip_digit():
        if strip == "Blue":
            return 4
        if strip == "White":
            return 1
        if strip == "Yellow":
            return 5
        return 1

    if color == "Blue" and text == "Abort":
        return ("hold", strip_digit())
    if batteries > 1 and text == "Detonate":
        return ("press", None)
    if color == "White" and label == "CAR":
        return ("hold", strip_digit())
    if batteries > 2 and label == "FRK":
        return ("press", None)
    if color == "Yellow":
        return ("hold", strip_digit())
    if color == "Red" and text == "Hold":
        return ("press", None)
    return ("hold", strip_digit())


def solve_keypads(data):
    syms = data["symbols"]
    cps = [ord(s) for s in syms]
    # treat U+0180 as a variant of U+048A for column matching
    def norm(cp):
        return 0x048A if cp == 0x0180 else cp
    norm_cps = [norm(cp) for cp in cps]
    # map keypad positions (1-4) to original symbols
    pos_map = {cps[i]: i + 1 for i in range(4)}
    for col in KEYPAD_COLUMNS:
        if all(ncp in col for ncp in norm_cps):
            # order by column position of normalized symbol
            ordered = sorted(cps, key=lambda cp: col.index(norm(cp)))
            positions = [str(pos_map[cp]) for cp in ordered]
            return " ".join(positions)
    # fallback: keep given order
    return " ".join(str(i + 1) for i in range(4))


def solve_complicated(data, bomb):
    results = []
    for color, led, star in zip(data["colors"], data["leds"], data["stars"]):
        red = 1 if "Red" in color else 0
        blue = 1 if "Blue" in color else 0
        letter = COMPLICATED_TABLE[(red, blue, 1 if star else 0, 1 if led else 0)]
        cut = False
        if letter == "C":
            cut = True
        elif letter == "D":
            cut = False
        elif letter == "S":
            cut = bomb["last_digit"] % 2 == 0
        elif letter == "P":
            cut = "parallel" in bomb["ports"]
        elif letter == "B":
            cut = bomb["batteries"] >= 2
        results.append("cut" if cut else "skip")
    return results


def parse_list_str(value):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1].strip()
    if not value:
        return []
    parts = [p.strip() for p in value.split(",")]
    # strip quotes if present
    return [p.strip("'").strip('"') for p in parts]


def parse_bool_list(value):
    return [v.strip().lower() == "true" for v in parse_list_str(value)]


def parse_module_data(module, data_str):
    try:
        if module == "Wires":
            amount_m = RE_AMOUNT.search(data_str)
            colors_m = RE_COLORS.search(data_str)
            if not amount_m or not colors_m:
                return None
            amount = int(amount_m.group(1))
            colors = parse_list_str(colors_m.group(1))
            return {"amount": amount, "colors": colors}
        if module == "Keypads":
            symbols_m = RE_SYMBOLS.search(data_str)
            if not symbols_m:
                return None
            symbols = parse_list_str(symbols_m.group(1))
            return {"symbols": symbols}
        if module == "Complicated Wires":
            amount_m = RE_AMOUNT.search(data_str)
            colors_m = RE_COLORS.search(data_str)
            leds_m = RE_LEDS.search(data_str)
            stars_m = RE_STARS.search(data_str)
            if not amount_m or not colors_m or not leds_m or not stars_m:
                return None
            amount = int(amount_m.group(1))
            colors = parse_list_str(colors_m.group(1))
            leds = parse_bool_list(leds_m.group(1))
            stars = parse_bool_list(stars_m.group(1))
            return {"amount": amount, "colors": colors, "leds": leds, "stars": stars}
        if module == "Button":
            color_m = RE_COLOR.search(data_str)
            text_m = RE_TEXT.search(data_str)
            strip_m = RE_STRIP.search(data_str)
            if not color_m or not text_m or not strip_m:
                return None
            color = color_m.group(1)
            text = text_m.group(1)
            strip = strip_m.group(1)
            return {"color": color, "text": text, "color_strip": strip}
    except Exception:
        return None
    return None


def parse_module(text):
    module_m = MODULE_RE.search(text)
    if not module_m:
        return None, None
    module = module_m.group(1).strip()
    data_m = DATA_RE.search(text)
    data = ast.literal_eval(data_m.group(1)) if data_m else {}
    return module, data


def main():
    host = "scripting.ctf.pascalctf.it"
    port = 6004

    sock = socket.create_connection((host, port), timeout=10)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    # read header up to first prompt
    data = read_until(sock, b"press Enter", timeout=1.2)
    text = data.decode("utf-8", errors="ignore")
    if "\x1b[" in text:
        text = ANSI_RE.sub("", text)
    bomb = parse_header(text)

    modules_solved = 0
    # prime first module
    sock.sendall(b"\n")
    while True:
        data = read_until(sock, b"Enter your solution", timeout=0.6)
        text = data.decode("utf-8", errors="ignore")
        if "\x1b[" in text:
            text = ANSI_RE.sub("", text)
        if "Game Over" in text or "BOOM" in text or "TIME'S UP" in text:
            sys.stdout.buffer.write(text.encode("utf-8", errors="ignore"))
            sys.stdout.buffer.write(f"\nSolved: {modules_solved}\n".encode("utf-8"))
            sys.stdout.buffer.flush()
            break
        if (
            "Congratulations" in text
            or "Bomb defused" in text
            or "bomb defused" in text
            or "Flag" in text
            or "flag" in text
        ):
            sys.stdout.buffer.write(text.encode("utf-8", errors="ignore"))
            sys.stdout.buffer.flush()
            break
        module, mdata = parse_module(text)
        if not module:
            continue

        if module == "Wires":
            cut = solve_wires(mdata, bomb)
            sock.sendall(f"{cut}\n\n".encode("utf-8"))
        elif module == "Button":
            action, digit = solve_button(mdata, bomb)
            if action == "press":
                sock.sendall(b"1\n\n")
            else:
                sock.sendall(f"2\n{digit}\n\n".encode("utf-8"))
        elif module == "Keypads":
            seq = solve_keypads(mdata)
            sock.sendall((seq + "\n\n").encode("utf-8"))
        elif module == "Complicated Wires":
            answers = solve_complicated(mdata, bomb)
            payload = "\n".join(answers) + "\n\n"
            sock.sendall(payload.encode("utf-8"))
        else:
            raise ValueError(f"Unknown module: {module}")

        modules_solved += 1

    sock.close()


if __name__ == "__main__":
    main()
```

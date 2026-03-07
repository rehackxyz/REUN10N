# forensic - painter

Solved by:p5yd4wk

we received a pcap of usb output
after analyzing i realized that this is actually a USB HID data from a tablet or mousepad. Our job is to reconstruct what was drawn
the concept is simple 1 for up, 0 for down soooo this is the script used:

```
#!/usr/bin/env python3
import subprocess
from PIL import Image, ImageDraw

tshark = r"C:\Program Files\Wireshark\tshark.exe"
pcap_file = "pref.pcap"

# Extract USB capdata
result = subprocess.run(
    [tshark, "-r", pcap_file, "-T", "fields", "-e", "usb.capdata"],
    capture_output=True, text=True, timeout=60
)

lines = [l.strip() for l in result.stdout.split('\n') if l.strip()]
print(f"[*] Parsing {len(lines)} HID reports...")

# Parse all reports
events = []
for line in lines:
    raw = bytes.fromhex(line.replace(':', ''))
    if len(raw) >= 7:
        btn = raw[0]
        pen_down = raw[1]  # 0=up, 1 or 2 = drawing
        x_delta = int.from_bytes(raw[2:4], 'little', signed=True)
        y_delta = int.from_bytes(raw[4:6], 'little', signed=True)
        events.append((pen_down, x_delta, y_delta))

# Calculate cumulative positions and find bounds
positions = []
x, y = 0, 0
for pen_down, dx, dy in events:
    x += dx
    y += dy
    positions.append((x, y, pen_down))

x_coords = [p[0] for p in positions]
y_coords = [p[1] for p in positions]
x_min, x_max = min(x_coords), max(x_coords)
y_min, y_max = min(y_coords), max(y_coords)

print(f"[+] Drawing bounds: X=[{x_min}, {x_max}], Y=[{y_min}, {y_max}]")
print(f"[+] Size: {x_max - x_min} x {y_max - y_min}")

# Create image with padding
padding = 50
width = (x_max - x_min) + 2 * padding
height = (y_max - y_min) + 2 * padding

print(f"[+] Image size: {width} x {height}")

# Render the drawing
img = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(img)

# Draw the path
prev_x, prev_y = None, None
for cx, cy, pen_down in positions:
    # Normalize coordinates
    nx = cx - x_min + padding
    ny = cy - y_min + padding

    if pen_down != 0 and prev_x is not None:
        # Pen is down - draw a line from previous position
        draw.line([(prev_x, prev_y), (nx, ny)], fill='black', width=2)

    prev_x, prev_y = nx, ny

img.save('reconstructed_drawing.png')
print(f"[+] Saved to reconstructed_drawing.png")

# Also try with different pen colors for byte1=1 vs byte1=2
img2 = Image.new('RGB', (width, height), 'white')
draw2 = ImageDraw.Draw(img2)

prev_x, prev_y = None, None
for cx, cy, pen_down in positions:
    nx = cx - x_min + padding
    ny = cy - y_min + padding

    if pen_down != 0 and prev_x is not None:
        color = 'blue' if pen_down == 1 else 'red'
        draw2.line([(prev_x, prev_y), (nx, ny)], fill=color, width=2)

    prev_x, prev_y = nx, ny

img2.save('reconstructed_drawing_colored.png')
print(f"[+] Saved colored version to reconstructed_drawing_colored.png")

print("\n[!!!] Drawing reconstructed! Open the PNG files to see what was painted.")
```
flag: `EH4X{wh4t_c0l0ur_15_th3_fl4g}`


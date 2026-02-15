# crypto - baby-rsa

SOLVED by OS1RIS

Flag: `pascalCTF{Wh41t_wh0_4r3_7h0s3_9uy5???}⁩`

-Convert colors to binary (black→0, white→1)
-Group into 8-bit chunks and convert to ASCII

```
from PIL import Image

def extract_border_binary(image_path):
    img = Image.open(image_path)
    img = img.convert("RGB")
    width, height = img.size
    
    # Generate border coordinates in same order as chal.py
    coords = []
    
    # Top edge: left to right
    for x in range(width):
        coords.append((x, 0))
    
    # Right edge: top to bottom (excluding first and last)
    for y in range(1, height-1):
        coords.append((width-1, y))
    
    # Bottom edge: right to left (if height > 1)
    if height > 1:
        for x in range(width-1, -1, -1):
            coords.append((x, height-1))
    
    # Left edge: bottom to top (excluding first and last, if width > 1)
    if width > 1:
        for y in range(height-2, 0, -1):
            coords.append((0, y))
    
    # Extract binary from border pixels
    binary_str = ""
    for coord in coords:
        pixel = img.getpixel(coord)
        # Black (0,0,0) = '0', White (255,255,255) = '1'
        if pixel == (0, 0, 0):
            binary_str += '0'
        elif pixel == (255, 255, 255):
            binary_str += '1'
        else:
            # Handle slight color variations if any
            brightness = sum(pixel) / 3
            binary_str += '0' if brightness < 128 else '1'
    
    return binary_str, coords

def binary_to_message(binary_str):
    message = ""
    # Process in chunks of 8 bits
    for i in range(0, len(binary_str), 8):
        chunk = binary_str[i:i+8]
        if len(chunk) == 8:
            char_code = int(chunk, 2)
            if 32 <= char_code <= 126:  # Printable ASCII
                message += chr(char_code)
            else:
                message += f"[{char_code}]"
    return message

# Convert to message
message = binary_to_message(binary_data)
print(f"{message}")
```

Solved by: yappare
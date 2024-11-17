# Quick Recovery

Solved by: @Who1sm3

## Question:
Hey, check this QR code ASAP! It's highly sensitive so I scrambled it, but you shouldn't have a hard time reconstructing - just make sure to update the a_order to our shared PIN. The b_order is the reverse of that 😉

## Solution:
```
from PIL import Image, ImageDraw
from itertools import permutations
import pyzbar.pyzbar as pyzbar

# Load the scrambled QR code image
qr_code_image = Image.open("qr_code.png")
width, height = qr_code_image.size
half_width, half_height = width // 2, height // 2

# Define the quadrants
squares = {
    "1": (0, 0, half_width, half_height),           # Top-left
    "2": (half_width, 0, width, half_height),       # Top-right
    "3": (0, half_height, half_width, height),      # Bottom-left
    "4": (half_width, half_height, width, height)   # Bottom-right
}

# Function to split a square into two triangles
def split_square_into_triangles(img, box):
    x0, y0, x1, y1 = box
    a_triangle_points = [(x0, y0), (x1, y0), (x0, y1)]
    b_triangle_points = [(x1, y1), (x1, y0), (x0, y1)]

    def crop_triangle(points):
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.polygon(points, fill=255)
        triangle_img = Image.new("RGBA", img.size)
        triangle_img.paste(img, (0, 0), mask)
        return triangle_img.crop((x0, y0, x1, y1))

    return crop_triangle(a_triangle_points), crop_triangle(b_triangle_points)

# Split each quadrant into triangles
triangle_images = {}
for key, box in squares.items():
    triangle_images[f"{key}a"], triangle_images[f"{key}b"] = split_square_into_triangles(
        qr_code_image, box)

# Generate all possible permutations
numbers = ["1", "2", "3", "4"]
permutations_list = list(permutations(numbers))

# Iterate over all combinations
for a_order in permutations_list:
    for b_order in permutations_list:
        reconstructed_image = Image.new("RGBA", qr_code_image.size)
        final_positions = [
            (0, 0),                       # Top-left
            (half_width, 0),              # Top-right
            (0, half_height),             # Bottom-left
            (half_width, half_height)     # Bottom-right
        ]
        for i in range(4):
            a_triangle = triangle_images[f"{a_order[i]}a"]
            b_triangle = triangle_images[f"{b_order[i]}b"]
            combined_square = Image.new("RGBA", (half_width, half_height))
            combined_square.paste(a_triangle, (0, 0))
            combined_square.paste(b_triangle, (0, 0), b_triangle)
            reconstructed_image.paste(combined_square, final_positions[i])
        
        # Attempt to decode the QR code
        decoded_objects = pyzbar.decode(reconstructed_image)
        if decoded_objects:
            print(f"Found QR code with a_order={a_order}, b_order={b_order}")
            for obj in decoded_objects:
                print("Data:", obj.data.decode('utf-8'))
            # Save the successfully reconstructed image
            reconstructed_image.save("reconstructed_qr_code.png")
            break
    else:
        continue
    break
    ```
**Flag:** `INTIGRITI{7h475_h0w_y0u_r3c0n57ruc7_qr_c0d3}`

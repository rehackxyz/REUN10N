# OS Detection

Solved by: @Zeqzoq

## Question:
Legendary pirate Bluebeard has travelled far and wide over the Deep Blue Sea and has seen every corner of it. The crew’s legendary ship, the Blue Pearl, is just as legendary. As is Bluebeard’s famous cutlass, and parrot, and eyepatch, and so on. Almost as legendary is Bluebeard’s ancient treasure map, on which parts of the Sea are said to be marked with blots of crimson ink. There, Bluebeard has buried countless treasures over the years. But the biggest treasure can only be found if all other stashes are discovered. Then, the legend goes, the Depth of the Sea at their locations points to where Bluebeard’s most enormous treasure lies, buried beneath the waves of the Deep Blue Sea itself.

Or so they say. You, a renowned treasure hunter, have paid a lot for the soggy piece of parchment now lying in front of you. It smells of seaweed and rip-off. You decide that it’s time to slowly peel it open and see if the Sea has left over anything of Bluebeard’s notes.


## Solution:
1. unzip the ora file then got layer0 and layer1 in data folder
2. extract red dot coordinate from layer0
3. map with pixel value layer1
4. then chatgpt to visualise the mapping

![4](https://i.ibb.co/cFK0vwV/map.png)

```
from PIL import Image

def extract_red_dots(image):
    """
    Extract coordinates of red dots from an image (where R > 0 and G = B = 0).
    """
    red_dot_coords = []
    width, height = image.size
    pixels = image.load()
    
    for x in range(width):
        for y in range(height):
            r, g, b, _ = pixels[x, y]  # Assuming RGBA
            if r > 0 and g == 0 and b == 0:  # Red dot condition
                red_dot_coords.append((x, y))
    
    return red_dot_coords

def decode_blue_channel_dynamically(red_dot_coords, layer1_image):
    """
    Dynamically decode the blue channel values at red dot coordinates in layer1, 
    ordered left-to-right, top-to-bottom.
    """
    # Sort coordinates: first by y (top-to-bottom), then by x (left-to-right)
    sorted_coords = sorted(red_dot_coords, key=lambda coord: (coord[1], coord[0]))

    # Access pixel values for the sorted coordinates in layer1
    layer1_pixels = layer1_image.load()
    blue_channel_values = [layer1_pixels[coord][2] for coord in sorted_coords]

    # Decode blue channel values to ASCII characters
    decoded_message = ''.join(chr(b) for b in blue_channel_values if 32 <= b <= 126)
    return decoded_message, sorted_coords

# File paths
layer0_path = "layer0.png"
layer1_path = "layer1.png"
try:
    # Open layer0 and layer1 images
    layer0_image = Image.open(layer0_path).convert("RGBA")
    layer1_image = Image.open(layer1_path).convert("RGBA")

    # Extract red dot coordinates from layer0
    red_dot_coords = extract_red_dots(layer0_image)

    # Decode the blue channel values dynamically
    decoded_message, sorted_coords = decode_blue_channel_dynamically(red_dot_coords, layer1_image)

    # Print results
    print("Decoded Message:", decoded_message)
    for coord, char in zip(sorted_coords, decoded_message):
        print(f"{coord}: '{char}'")
except Exception as e:
    print(f"Error: {e}")
    ```
    
**Flag:** `PP{f1L3_F0rm4t5_4r3_a_Tr345uR3_tR0v3}`

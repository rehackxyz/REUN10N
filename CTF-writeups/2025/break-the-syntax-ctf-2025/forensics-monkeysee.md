# Solution

```py
import pyshark
import string
import sys

KEY_MAP = {
    4: "a", 5: "b", 6: "c", 7: "d", 8: "e", 9: "f", 10: "g", 11: "h",
    12: "i", 13: "j", 14: "k", 15: "l", 16: "m", 17: "n", 18: "o", 19: "p",
    20: "q", 21: "r", 22: "s", 23: "t", 24: "u", 25: "v", 26: "w", 27: "x",
    28: "y", 29: "z", 30: "1", 31: "2", 32: "3", 33: "4", 34: "5", 35: "6",
    36: "7", 37: "8", 38: "9", 39: "0", 40: "\n", 41: "[ESC]", 42: "[DEL]",
    43: "\t", 44: " ", 45: "_", 47: "{", 48: "}", 50: "#", 52: "[SHIFT]",
    54: ",", 55: ".", 56: "/", 57: "[CAPS]", 79: "→", 80: "←"
}

def get_data(file_name):
    return [
        pkt.data.usb_capdata.replace(':', '')
        for pkt in pyshark.FileCapture(file_name, display_filter='frame.len == 73')
        if hasattr(pkt.data, 'usb_capdata') and pkt.data.usb_capdata != '00:00:00:00:00:00:00:00'
    ]

def map_keystrokes(data):
    keypresses = []
    for line in data:
        for byte in bytearray.fromhex(line.strip()):
            if byte and byte in KEY_MAP:
                keypresses.append(KEY_MAP[byte])

    output = []
    for key in keypresses:
        if key == "[DEL]":
            if output: output.pop()
        else:
            output.append(key)
    print(''.join(output))

if __name__ == '__main__':
    map_keystrokes(get_data(sys.argv[1]))
```

Flag: `BtSCTF{m0nk3y_tYpE!!1!!oneone!}`

## Referrence
https://afnom.net/wtctf/2019/the_story_of_a_monkey/

Solved by: n3r

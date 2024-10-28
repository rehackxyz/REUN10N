# my-assm-hurts

Solved by: @n3r

## Question:
As Mary was attempting to time travel, she slipped on a patch of ice and landed on her butt. While getting up from the ice, she found a cool-looking USB flash drive containing a file with some system code. Can you help Mary decrypt what information the file has?


## Solution:
1. `strings freezingprogram.txt | grep hold` (look how each character being declared)
2. then rawdogging the asm (or convert it to py)

```py
class Emulator:
    def __init__(self):
        self.registers = {'r' + str(i): 0 for i in range(10)}  # 10 registers
        self.memory = {}
        self.stack = []
        self.vtables = {
            'Bool': ['Object.abort', 'Object.copy', 'Object.type_name'],
            'IO': ['Object.abort', 'Object.copy', 'Object.type_name', 'IO.in_int', 'IO.in_string', 'IO.out_int', 'IO.out_string'],
            # Define vtables for other classes as needed
        }
        # Updated strings to match the values in freezingprogram.txt
        self.strings = {
            "string8": "N",
            "string10": "I",
            "string12": "C",
            "string15": "{",
            "string17": "h",
            "string19": "E",
            "string21": "y",
            "string23": "_",
            "string25": "t",
            "string28": "1",
            "string30": "s",
            "string32": "-",
            "string34": "i",
            "string39": "o",
            "string41": "0",
            "string43": "L",
            "string45": "}",
        }
        self.flag = ""

    def execute_main(self):
        """Simulate Main.main to construct the flag."""
        # Concatenating strings to simulate the assembly's flag construction
        self.flag += self.strings["string8"]
        self.flag += self.strings["string10"]
        self.flag += self.strings["string12"]
        self.flag += self.strings["string12"]
        self.flag += self.strings["string15"]
        self.flag += self.strings["string17"]
        self.flag += self.strings["string19"]
        self.flag += self.strings["string21"]
        self.flag += self.strings["string23"]
        self.flag += self.strings["string25"]
        self.flag += self.strings["string17"]
        self.flag += self.strings["string28"]
        self.flag += self.strings["string30"]
        self.flag += self.strings["string32"]
        self.flag += self.strings["string34"]
        self.flag += self.strings["string30"]
        self.flag += self.strings["string23"]
        self.flag += self.strings["string12"]
        self.flag += self.strings["string39"]
        self.flag += self.strings["string41"]
        self.flag += self.strings["string43"]
        self.flag += self.strings["string45"]

        print(f"Flag: {self.flag}")

# Instantiate and run
emulator = Emulator()
emulator.execute_main()
```


**Flag:** `NICC{hEy_th1s-is_Co0L}`

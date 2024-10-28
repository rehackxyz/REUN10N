# the-moth-flies-at-dawn

Solved by: @hikki

## Question:
NICC is on the hunt for the elusive moth-man! In order to draw him out of hiding, we need to cook a nice breakfast for him. Luckily, one of our agents has recovered a hash of the cryptid's favorite breakfast. Crack the hash and serve up a great breakfast!


## Solution:
```
def mycipher(myinput):
    global myletter
    rawdecrypt = list(myinput)
    encrypted = []

    for iter in range(len(rawdecrypt)):
        encrypted_char = (ord(rawdecrypt[iter]) + myletter)

        # Ensure the result is a printable ASCII character
        if encrypted_char < 32:  # If less than space, wrap to printable range
            encrypted_char += 95  # Wrap into printable range
        elif encrypted_char > 126:  # If greater than tilde, wrap around
            encrypted_char = 32 + (encrypted_char - 127)

        encrypted.append(chr(encrypted_char))
        myletter = (myletter + 1) % 256  # Increment myletter and wrap around at 256

    return "NICC{" + ''.join(encrypted) + "}"

def encrypt_file_and_print(input_file):
    global myletter
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    encrypted_content = mycipher(content)
    print(encrypted_content)

input_filename = "flag.output"


for i in range(0, 128):
    myletter = i
    print("key:", i)
    encrypt_file_and_print(input_filename)
```

**Flag:** `NICC{WAt_dO_yOu_tHINk_of_My_cIpHer}`

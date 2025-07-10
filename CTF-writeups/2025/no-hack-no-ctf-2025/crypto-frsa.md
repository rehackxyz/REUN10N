Extract the symbol stream, compute symbol frequencies, build a substitution mapping, decode the full message

```
# decode_frsa_flag_template.py

def load_cipher_symbols(filepath):
    with open(filepath, 'r') as f:
        return f.read().split()

def decode_symbols(symbols, mapping):
    return ''.join(mapping.get(sym, '*') for sym in symbols)

def extract_flag_line(decoded_text, keyword="FLAG"):
    words = decoded_text.split()
    for i in range(len(words)):
        if keyword in words[i]:
            return ' '.join(words[max(i-4, 0):i+5])
    return "FLAG not found."

if __name__ == "__main__":
    # Step 1: Load cipher symbols
    filepath = "cipher_symbols.txt"  # change if needed
    symbols = load_cipher_symbols(filepath)

    # Step 2: Fill in your mapping here
    mapping = {
        'SYM00': ' ',
        'SYM01': 'E',
        'SYM02': 'T',
        'SYM03': 'I',
        'SYM04': 'A',
        'SYM05': 'S',
        'SYM06': 'N',
        'SYM07': 'O',
        'SYM08': 'H',
        'SYM09': 'R',
        'SYM10': 'D',
        'SYM11': 'M',
        'SYM12': 'L',
        'SYM13': 'F',
        'SYM14': 'C',
        'SYM15': 'G',
        'SYM16': 'Y',
        'SYM17': 'U',
        'SYM18': 'W',
        'SYM19': 'B',
        'SYM20': 'K',
        'SYM21': 'V',
        'SYM22': 'P',
        'SYM23': 'Q',
        'SYM24': 'X',
        'SYM25': 'J',
        'SYM26': 'Z',
    }

    # Step 3: Decode the message
    decoded_text = decode_symbols(symbols, mapping)

    # Step 4: Output
    print("----- FULL DECODED MESSAGE -----")
    print(decoded_text)

    print("\n----- FLAG CONTEXT -----")
    print(extract_flag_line(decoded_text, "NHNC"))


``` 

NHNC{THIS_IS_RSA_AND_FREQUENCY_ANALYSIS}

Solved by: jiqqyy
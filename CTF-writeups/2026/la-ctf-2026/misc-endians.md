# misc - endians

```
def decode_challenge(encoded_text: str) -> str:
    """
    Decode the challenge text by reversing the endian encoding.

    Each Chinese character represents a UTF-16LE encoded ASCII character.
    The Unicode code point's high byte is the ASCII value.
    """
    decoded_bytes = bytearray()

    for char in encoded_text:
        code_point = ord(char)
        # Extract the high byte (ASCII value) from the UTF-16LE pair
        # U+6C00 -> 0x6C = 'l'
        decoded_bytes.append(code_point >> 8)

    return decoded_bytes.decode('ascii')


def encode_challenge(text: str) -> str:
    """
    Reproduce the challenge encoding for verification.

    Encode as UTF-16LE, then decode as UTF-16BE to get Chinese characters.
    """
    return text.encode('utf-16le').decode('utf-16be')


def main():
    # The encoded text from chall.txt
    encoded = "氀愀挀琀昀笀㄀开猀甀爀㌀开栀　瀀攀开琀栀㄀猀开搀　攀猀开渀　琀开最㌀琀开氀　猀琀开㄀渀开琀爀愀渀猀氀愀琀椀　渀℀紀"

    print("=" * 60)
    print("LA CTF Endian Encoding Challenge Solver")
    print("=" * 60)

    print(f"\n[+] Encoded text: {encoded}")
    print(f"[+] Length: {len(encoded)} characters")

    # Decode the flag
    flag = decode_challenge(encoded)
    print(f"\n[+] Decoded flag: {flag}")

    # Verify by re-encoding
    verify = encode_challenge(flag)
    print(f"\n[+] Verification (re-encoded): {verify}")
    print(f"[+] Match: {verify == encoded}")

    # Show some examples of the encoding
    print("\n[+] Encoding examples:")
    for char in flag[:10]:
        encoded_char = encode_challenge(char)
        print(f"    '{char}' -> U+{ord(encoded_char):04X} -> '{encoded_char}'")

    print("\n" + "=" * 60)
    print(f"FLAG: {flag}")
    print("=" * 60)


if __name__ == "__main__":
    main()
```
Flag: `lactf{1_sur3_h0pe_th1s_d0es_n0t_g3t_l0st_1n_translati0n!}`

SOLVED by WannaBeMeButTakJadi

Solved by: yappare
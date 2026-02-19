# misc - emojis

file is near useless. copy the title and description. on the title and description got hidden hex character

```
def decode_hidden_tags(text, offset=16):
    """
    Extracts hidden Unicode tags and applies a Caesar shift/offset.
    """
    decoded_chars = []

    for char in text:
        codepoint = ord(char)

        # Check if the character is in the Unicode Tag block (U+E0000 - U+E01FF)
        if 0xE0000 <= codepoint <= 0xE01FF:
            # 1. Normalize the tag (subtract the start of the block)
            # Most common CTF start points are 0xE0000 or 0xE0100
            tag_value = codepoint - 0xE0100

            # 2. Apply the discovered offset (+16)
            ascii_value = tag_value + offset

            # 3. Convert back to a readable character
            decoded_chars.append(chr(ascii_value))

    return "".join(decoded_chars)

# Input strings from the challenge
title_str = "Emo󠄠󠅨󠅖󠅥󠅞ji's"
desc_str = "something seems to be in here 🤔󠅞󠅟󠅤󠅘󠅙?"

print(f"{decode_hidden_tags(title_str)}")
# 0xfun{3moji_s3cr3t_emb3d_1n_t1tle}
```

Flag: `0xfun{3moji_s3cr3t_emb3d_1n_t1tle}`

Solved by OS1RIS

Solved by: ha1qal
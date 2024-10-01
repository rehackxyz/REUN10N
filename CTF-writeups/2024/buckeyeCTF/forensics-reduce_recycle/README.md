# reduce_recycle

Solved by: @yappare

### Question
I forgot the randomly generated 12-character password I used to encrypt these files.... is there anything you can do to help me get my flag back??

### Solution:

Use `bkcrack` to extract `dogs_wearing_tools.zip`. Set the plaintext to PNG header to get the keys.
`./bkcrack-1.7.0-Linux/bkcrack -C dogs_wearing_tools.zip -c 4.png -p plain.txt`

Once obtained the keys, bruteforce the password using `bkcrack`
`./bkcrack-1.7.0-Linux/bkcrack  -k keyss --bruteforce ?p --length 12`

Extract the `important_flags.7z` using the recovered password.

**Flag:** `bctf{wH1ch_d0g_w4s_youR_FaVOr1t3} `

# photo-clue

Solved by: @n3r

## Question:
A seemingly innocuous old photo file has emerged, but Mary Morse suspects it may hold the key to deciphering The Consortium's next move. Your task is to analyze the metadata, uncover the true nature of the file, and submit the flag before The Consortium acts. Time is running out—can you crack the mystery behind the photo?

(Note: If you choose to use volatility2.6, use profile Win10x64_19041)

## Solution:
1. search for `.jpg `in the memory dump` vol.py -f Challenge3.raw windows.filescan | grep ".jpg"`
2. dump it `vol -f Challenge3.raw -o "./filedump" windows.dumpfiles --virtaddr <offset>`
3. extract the photo using https://www.aperisolve.com/ (donno why steghide can't do this without password)
4. crack the `.pdf` `john REDACTED-protected.hash --wordlist=/usr/share/wordlist/rockyou.txt`
5. open it with the password, convert the binary to ascii

**Flag:** `NICC{M0rse_Ph0t0_S3crets}`

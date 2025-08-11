## Description
With everything and everyone going AI today, we also are developing our own AI bot. It is a first draft and it still requires some work, but feel free to test it out.

> Connection:
> 
> nc simple-ai-bot.ctf.zone 4242

## Solution

This is a blind remote challenge (no challenge file given). We can try and spam strings but it only scans your input up until a certain length so no overflow. We do however have a printf vulnerability so we can read values off of the stack. When we enter `flag`, it also gives us the address of the flag, i.e `0x60811ca4d040` meaning it's on the heap and it's a 64bit system.
We can then use the printf vulnerability to read the value at that address to get the flag.

Flag: `flag{bee82de11dda03908f3f3d41e2795cdf}`

Solved by: benkyou
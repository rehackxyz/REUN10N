Solved by: @OS1R1S

### Question:
It's a simple SNES game of Snake… or is it? Each apple you eat reveals a letter, but before you can spell out the full flag, the apples run out.

If only there were another way to uncover the secret… perhaps by diving into the depths of 65816 assembly and extracting the flag directly from the game's code?

Can you outsmart the limitations and claim your prize?

### Solution:
- Use mesen emulator's memory viewer to freeze points. The every collected apple was +02 in hex. $1A was the address. if die, just change the last point.
![[rev1.png]]

Here is how we can extract the hex value from the memory view and notice the hex value changes per apple taken.
![rev2](rev2.gif)

**Flag:** `KALMAR{EASY_PEASY_65816_SQUEEZY}


# Puzzle Room

Solved by: @hikki

- Category: reverse
- Description:

As you delve deeper into the tomb in search of answers, you stumble upon a puzzle room, its floor entirely covered in pressure plates. The warnings of the great necromancer, who hid his treasure here, suggest that one wrong step could lead to your doom.

You enter from the center of the eastern wall. Although you suspect you’re missing a crucial clue to guide your steps, you’re confident that everything you need to safely navigate the traps is already within reach.

At the center of the room lies the key to venturing further into the tomb, along with the promise of powerful treasures to aid you on your quest. Can you find the path, avoid the traps, and claim the treasure (flag) on the central platform?

- Challenge File: puzzle\_room.py

## Tricks to solve:

- Dont step on same words
- Dont step on same column
- Dont step on into shrine with W
- Dont step on sphinx

With these steps, you will get these combination of movements to get the flag:
- SW
- SW
- SW
- NW
- SW
- NW
- W
- N

Summary of Game Rules:\
Stay within the grid boundaries.\
Avoid stepping on (3, 9) (the tile where the door landed).\
Avoid stepping on any "SPHINX" tiles.\
Do not revisit any tile you've already stepped on.\
Do not step on tiles with the same symbol more than once (except "Shrine").\
Ensure no two tiles in your path share the same column unless you're on a "Shrine" tile.\
The path must form a valid decryption key on "Shrine" tiles to win the game.\
tried to find a path that will include all the words\
snake arch plant bug staff foot urn Shrine

**Flag:** `pctf{Did_you_guess_it_or_apply_graph_algorithms?}`



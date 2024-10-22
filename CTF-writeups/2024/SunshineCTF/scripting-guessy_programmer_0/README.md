# Guessy Programmer 0

Solved by: @n3r

## Question:
Adventurer beware!

This challenge is not for the faint of heart.

Scour through the text. Find its innate meaning.

Find the red flags.

Find what you search for.

PS
Regular expressions are the weapon of a true programmer. Not as clumsy or random as a search engine; an elegant tool from a more civilized age.

([Oo][Bb][Ii])-+([Ww][Aa][Nn]) ?(K[Ee][Nn][Oo][Bb][iI])+

## Solution:
```
git clone <source> <destination>
strings adventurenovel.txt | grep "sun{" | grep "}"
```

**Flag:** `sun{w@it_w@s_1t_th@t_e@sy_r3g3x_is_n0t@f@ir@dventure_here_take_this_sun_flag{_secret_flag}`

# BotNet 1

Solved by: @vicevirus

## Question:
A bunch of robots have started a new Mastodon instance called BotNet... but wait! That's not Mastodon! What secrets are they hiding from us, and why is one user more secretive than the other?

(Submit flag_1 here)

(hint: this is not Mastodon-specific; read a bit on the protocol.)

## Solution:
`curl -s -H "Accept: application/activity+json" https://botnet.2024.sunshinectf.games/users/rin`

**Flag:** `sun{1_c4n_r34d_b0ts}`

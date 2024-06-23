# Misc - sh
Solved by **0x251e**\
Original writeup by 0x251e - https://medium.com/@shreethaar/wanictf-2024-sh-37eb1bb2ea63

## Question
Guess?
Challenge file: mis-sh.zip

## Solution

### Analsying game.sh
```
#!/usr/bin/env sh

set -euo pipefail

printf "Can you guess the number? > "

read i

if printf $i | grep -e [^0-9]; then
    printf "bye hacker!"
    exit 1
fi

r=$(head -c512 /dev/urandom | tr -dc 0-9)

if [[ $r == $i ]]; then
    printf "How did you know?!"
    cat flag.txt
else
    printf "Nope. It was $r."
fi
```

Based on shell script, it is prone to command injection from `set -euo pipefail` and `printf $i` statement is vulnerable to command injection, as it doesn't properly sanitize the user input.

### Exploiting

With `set -eou pipefail` we can bypass with `||` as it means if the first command fails it will run the second one.
Example: `cat flag.txt|| ls`

![1](https://miro.medium.com/v2/resize:fit:720/format:webp/1*tbKjbTQJaa6btOPypw1QWA.png)

### Flag
`FLAG{use_she11check_0r_7he_unexpec7ed_h4ppens}`

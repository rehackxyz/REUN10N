# Solution
```
curl -X POST "http://188.245.212.74:10001/personalized-quotes" \
-H "Content-Type: application/json" \
-d '{"name": "f.l.a.g"}'
```

Flag: `ping{fastify-more-like-slowify-hehe-anMtYW5keQ==}`
---

---
Category: Misc
Challenge Name: interview


# Solution
- check spectogram of interview.mp3 found phrase "Which One?" but Im not sure whats that
- steghide extract politechnika.jpg which no password get a zip file containing hint.txt and password protected zip file
- hint.txt said "What year it was..?"
- make a bruteforce script to file the zip file password and got `2011` as the password
- View the zip file then got flag

Flag: `ping{d0_y0u_4l50_60nn4_pl4y_70mb_r41d3r?}`


Solved by: yappare
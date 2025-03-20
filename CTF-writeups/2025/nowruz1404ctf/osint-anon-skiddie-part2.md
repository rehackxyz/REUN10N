# Anon Skidde Part2
Solved by: @apik

### Question:
This dude is really ambitious. He literally begged us to let him attend our post-event meeting and we said yes.

Since he's not good at time management, our organizer sent him the event's `.ics` file and asked him to import it to his calendar. What can go wrong?

### Solution:
- Using [ghunt]([https://github.com/mxrch/GHunt](https://github.com/mxrch/GHunt "https://github.com/mxrch/GHunt")) tool 

```
🗓 Calendar data

[+] Public Google Calendar found !

Calendar ID : h4ck3r.g0odr4tm4nd@gmail.com
Calendar Timezone : Asia/Tehran

[+] 1 event dumped ! Showing the last 1 one...

╔════════════════════╤═════════════════════╤═══════════════════╗
║        Name        │   Datetime (UTC)    │     Duration      ║
╟────────────────────┼─────────────────────┼───────────────────╢
║ Post Event Meeting │ 2025/03/16 16:00:00 │ 1 hour 30 minutes ║
╚════════════════════╧═════════════════════╧═══════════════════╝

🗃 Download link :
=> https://calendar.google.com/calendar/ical/h4ck3r.g0odr4tm4nd@gmail.com/public/basic.ics
```

The ics contains this:
```
DESCRIPTION:File attachment:<br><span>1PDw-S4ZXQbGuKBNayEz6XqtiA6tl1lcOBT4n
 I1IFaac</span>
```

go to dcode.fr and it detects as google drive link open link got docs with this base64-encoded flag

```
https://docs.google.com/document/d/1PDw-S4ZXQbGuKBNayEz6XqtiA6tl1lcOBT4nI1IFaac/
Rk1DVEZ7TTRZODNfMU1fbjA3XzdINDdfNG4wTnltMFU1fQ==
```

**Flag:** `FMCTF{M4Y83_1M_n07_7H47_4n0Nym0U5}`


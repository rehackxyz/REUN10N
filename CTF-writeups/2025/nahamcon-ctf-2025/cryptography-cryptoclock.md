### Solution

Vibe solved  
```
#!/usr/bin/env python3
import socket, re
from binascii import unhexlify

HOST, PORT = "challenge.nahamcon.com", 30603

def recv_until(sock, marker):
    data = b""
    while marker not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data

def main():
    banner = recv_until((s := socket.create_connection((HOST, PORT))), b"Enter text to encrypt")
    m = re.search(rb"encrypted flag is: ([0-9a-f]+)", banner, re.IGNORECASE)
    enc_flag_hex = m.group(1).decode()
    L = len(enc_flag_hex) // 2

    payload = b"A" * L + b"\n"
    s.sendall(payload)

    resp = recv_until(s, b"\n")
    m2 = re.search(rb"Encrypted: ([0-9a-f]+)", resp, re.IGNORECASE)
    enc_data_hex = m2.group(1).decode()

    C_flag = unhexlify(enc_flag_hex)
    C_data = unhexlify(enc_data_hex)
    flag = bytes(cf ^ (cd ^ 0x41) for cf, cd in zip(C_flag, C_data))

    print(flag.decode())

if __name__ == "__main__":
    main()
```  

Flag:`flag{0e42ba180089ce6e3bb50e52587d3724}`

Solved by: zeqzoq

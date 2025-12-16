```python
from pwn import *

def main():
    HOST = "public.ctf.r0devnull.team"
    PORT = 3010

    answers = [
        "RealSlimShady1337",
        "X0r3dS3crets!",
        "T1547.001",
        "Shadiest",
        "shadystealerconnect.tk",
        "notepad.exe",
        "FIN{50y0u41n7r34llysh4dy}",
    ]

    print(f"[*] Connecting to {HOST}:{PORT} ...")
    conn = remote(HOST, PORT)

    try:
        banner = conn.recvuntil(b"Question 1:", timeout=10)
        print(banner.decode(errors="ignore"), end="")
    except Exception as e:
        print(f"[!] Error receiving banner: {e}")

    for i, ans in enumerate(answers, start=1):
        try:
            prompt = conn.recvuntil(b"Your answer:", timeout=30)
            print(prompt.decode(errors="ignore"), end="")

            print(f"[*] Sending answer to Q{i}: {ans}")
            conn.sendline(ans.encode())
        except Exception as e:
            print(f"[!] Error while answering Q{i}: {e}")
            break
    conn.interactive()

if __name__ == "__main__":
    main()
```

Flag:  nullctf{St4rt1ng_Y0ur_M4lw4r3_C4r33r_41n't_H4rd!}

Solved by: warlocksmurf
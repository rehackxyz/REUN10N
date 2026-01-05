# Solution

```python
from pwn import *

def main():
    HOST = "public.ctf.r0devnull.team"
    PORT = 3007

    answers = [
        "HCPrMNUTufgxpxMSH",
        "WDS100T2B0A, F:",
        "QEMU DADY VirtualBox BOCHS_ BXPC___",
        "XPtZOUHY5OeenWFPBw1yCsPCGanSXRbZFoEprI16QF8= FRxUQwvJ84LwrFZMYH8pPg== CBC",
        "HKLM:\\SOFTWARE\\OOhhhm=",
        "Acwq",
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

Flag: nullctf{n3v3r_run_4ny7hing_y0u_find_0n_7h3_n37}

Solved by: warlocksmurf

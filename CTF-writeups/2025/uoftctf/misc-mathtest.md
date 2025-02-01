# Math Test

Solved by: @plssky

## Question:
Complete this simple math test to get the flag.

## Solution:
```
import socket
import re

def solve_equation(equation):
    try:
        result = eval(equation)
        return int(result)
    except:
        return None

def solve_challenge(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    while True:
        try:
            data = s.recv(4096).decode('utf-8')
            if not data:
                break
                
            print(data)  # Print everything from server
            
            if "Question:" in data:
                match = re.search(r'Question: (.*)', data)
                if match:
                    equation = match.group(1).strip()
                    answer = solve_equation(equation)
                    
                    if answer is not None:
                        response = f"{answer}\n"
                        print(f"Sending: {answer}")
                        s.send(response.encode())
        except:
            break

    s.close()

if __name__ == "__main__":
    HOST = "34.66.235.106"
    PORT = 5000
    
    solve_challenge(HOST, PORT)

```

**Flag:** `uoftctf{7h15_15_b451c_10_7357_d16u153d_45_4_m47h_7357}`

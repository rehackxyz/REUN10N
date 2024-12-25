# I Like McDonalds

Solved by: @cicakberlari

## Question:
My friend has created his own hashing service and has given it to me to crack it, can you help me with it. He has promised me a burger for this as I like McDonald's so much , can you help me get some? please :) :)


## Solution:
We need to input token 64 times and they give us 128 times to try. And if we input wrong token it will output the expected one. So we put the wrong token and resubmit the right one, and repeat it until we got the flag.

```
import socket
import re

def main():
    host = "34.45.235.239"
    port = 8004

    print(f"Connecting to {host}:{port}...")
    with socket.create_connection((host, port)) as sock:
        # Read the server's welcome message
        print(sock.recv(4096).decode())

        successes = 0
        for i in range(128):
            message = f"message-{i}".encode().hex()

            # Send an initial invalid token to get the expected token
            invalid_token = "deadbeefdeadbeef"
            submission = f"{message} {invalid_token}\n"
            sock.sendall(submission.encode())

            # Read the server's response
            response = sock.recv(4096).decode()
            print(f"Server response: {response}")

            # Extract the expected token
            match = re.search(r"Expected token: ([0-9a-f]+)", response)
            if not match:
                print("Failed to extract expected token. Exiting...")
                break

            expected_token = match.group(1)

            # Resubmit with the expected token
            submission = f"{message} {expected_token}\n"
            print(f"Submitting valid attempt {i+1}: {submission.strip()}")
            sock.sendall(submission.encode())

            # Read the success response
            response = sock.recv(4096).decode()
            print(f"Server response: {response}")

            if "Success!" in response:
                successes += 1
                print(f"Valid tokens accepted: {successes}/64")
                if successes >= 64:
                    print("Challenge completed successfully!")
                    break

if __name__ == "__main__":
    main()
```

**Flag:** `flag{}`

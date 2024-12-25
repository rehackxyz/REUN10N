# Burn it!

Solved by: @vicevirus

## Question:
Hey Ghost Hunter. You have come across a few cursed objects that have spirits attached to them.

These cursed objects are made up of knots that are connected by threads. The threads are connected in such a way that no cycles are formed. We need to burn these cursed objects to get rid of the spirits, but there is a catch. If while burning, the cursed object breaks into two, the spirit will be released and you will suffer a very bad death.

You can set fire to multiple knots at chosen points of time (time can't be negative) and the cursed object will start burning from those points at those particular times (two knots can start burning at the same time). Each thread takes 1 second to burn , so the fire can reach from one knot to an adjacent one in 1 second. Tell me which knots to burn at what time and if you burn all cursed objects you get the flag.


## Solution:
o1-mini supremacy

```
from pwn import *
import re
from collections import defaultdict, deque

# Disable Pwntools logging for cleaner output
context.log_level = 'debug'

def parse_input(data):
    """
    Parses the server's input data to extract the connections between knots.
    Returns a list of tuples representing the edges.
    """
    connections = []
    lines = data.strip().split('\n')
    for line in lines:
        match = re.match(r'(\d+)\s+(\d+)', line)
        if match:
            connections.append((int(match.group(1)), int(match.group(2))))
    return connections

def find_centers(adj):
    """
    Finds the central node(s) of the tree using the iterative leaf-removal method.
    Returns a list of central node(s).
    """
    degrees = {node: len(neighbors) for node, neighbors in adj.items()}
    leaves = deque([node for node, degree in degrees.items() if degree <= 1])
    removed = 0
    n = len(adj)
    
    while removed < n:
        size = len(leaves)
        if removed + size >= n:
            return list(leaves)
        removed += size
        for _ in range(size):
            leaf = leaves.popleft()
            for neighbor in adj[leaf]:
                degrees[neighbor] -= 1
                if degrees[neighbor] == 1:
                    leaves.append(neighbor)
    return []

def bfs(adj, start):
    """
    Performs BFS from the start node.
    Returns a dictionary mapping each node to its distance from the start node.
    """
    distances = {}
    queue = deque()
    queue.append((start, 0))
    visited = set()
    visited.add(start)
    
    while queue:
        node, dist = queue.popleft()
        distances[node] = dist
        for neighbor in adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return distances

def compute_burning_plan(connections):
    """
    Computes the burning plan by:
    1. Finding the central node(s).
    2. Calculating distances from all leaves to the central node(s).
    3. Determining burning times to synchronize fire arrival at the center.
    Returns the burning plan as a formatted string.
    """
    # Build the adjacency list
    adj = defaultdict(list)
    for u, v in connections:
        adj[u].append(v)
        adj[v].append(u)
    
    # Find central node(s)
    centers = find_centers(adj)
    
    # Perform BFS from all centers to get minimum distances
    distances = {}
    for center in centers:
        bfs_dist = bfs(adj, center)
        for node, dist in bfs_dist.items():
            if node not in distances or dist < distances[node]:
                distances[node] = dist
    
    # Identify leaves (degree == 1)
    leaves = [node for node in adj if len(adj[node]) == 1]
    
    # Calculate max distance from any leaf to the center
    max_distance = max(distances[leaf] for leaf in leaves)
    
    # Determine burning times
    burning_plan = []
    for leaf in leaves:
        distance = distances[leaf]
        burn_time = max_distance - distance
        burn_time = max(burn_time, 0)  # Ensure non-negative
        burning_plan.append((leaf, burn_time))
    
    # Sort burning_plan by time ascending and then by knot number for consistency
    burning_plan.sort(key=lambda x: (x[1], x[0]))
    
    # Remove duplicates if any (though in a tree, leaves are unique)
    unique_burning = []
    seen = set()
    for knot, time in burning_plan:
        if knot not in seen:
            unique_burning.append((knot, time))
            seen.add(knot)
    
    # Format the burning plan
    plan = f"{len(unique_burning)} " + " ".join(f"{knot} {time}" for knot, time in unique_burning)
    return plan

def main():
    # Server details
    HOST = '34.42.147.172'
    PORT = 8010

    try:
        # Establish connection to the server
        conn = remote(HOST, PORT)

        while True:
            # Receive data until the prompt
            try:
                received_data = conn.recvuntil(b"Enter the number of knots you want to burn as", timeout=10).decode(errors='ignore')
            except EOFError:
                print("Connection closed by the server.")
                break
            except Exception as e:
                print(f"An error occurred while receiving data: {e}")
                break

            if not received_data:
                print("No more data received. Exiting.")
                break

            # Debug: Print the received data
            print("\n--- Received Data ---")
            print(received_data)
            print("----------------------\n")

            # Extract the connections part
            # Assuming the connections are listed after the colon and newline
            try:
                connections_part = received_data.split(': \n')[-1]
                connections = parse_input(connections_part)
            except IndexError:
                print("Failed to parse connections. Exiting.")
                break

            # Debug: Print the parsed connections
            print("Parsed Connections:")
            print(connections)
            print("---------------------\n")

            if not connections:
                print("No connections found. Exiting.")
                break

            # Compute the burning plan
            burning_plan = compute_burning_plan(connections)
            print(f"Computed Burning Plan: {burning_plan}\n")

            # Send the burning plan
            conn.sendline(burning_plan.encode())

            # Receive the server's response after sending the burning plan
            try:
                response = conn.recvline(timeout=5).decode(errors='ignore').strip()
            except EOFError:
                print("Connection closed by the server after sending burning plan.")
                break
            except Exception as e:
                print(f"An error occurred while receiving response: {e}")
                break

            # Debug: Print the server's response
            print("--- Server Response ---")
            print(response)
            print("------------------------\n")

            # Check for failure message
            if "Oh no! The fire broke off" in response:
                print("🔥 **Burning plan failed:** The fire broke off.")
                print(f"**Response from server:** {response}")
                break

            # Check for success message
            elif "Well Done!" in response:
                print("✅ **Burning plan succeeded!**")
                print(f"**Response from server:** {response}\n")
                # Continue to the next cursed object or terminate if completed
                continue

            else:
                # Handle unexpected responses
                print(f"⚠️ **Unexpected response from server:** {response}\n")
                continue

        # Close the connection
        conn.close()
        print("🔒 **Connection closed.**")

    except EOFError:
        print("Connection closed by the server.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
message.txt
```

**Flag:** `flag{Ghost_Hunting_101_:_Don't_Upload_your_chall_without_testing}`

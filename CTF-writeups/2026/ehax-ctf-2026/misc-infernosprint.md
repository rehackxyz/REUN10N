# misc - inferno sprint

Solved by: p5yd4wk

this chall requires you to survive 5 rounds of mazes. Each round got challenges and all.
after playing for few minutes, i made a script to autoplay and get the flag
script explanation is commented inside the code 


flag: `EH4X{1nf3rn0_spr1n7_bl4z3_runn3r_m4573r} `
```python3
#!/usr/bin/env python3

import socket
import time
import binascii
from collections import deque
from typing import List, Tuple, Optional, Set, Dict

class FireMazeSolver:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = None
        self.maze = []
        self.start_pos = None
        self.portals = {}  # portal_id -> list of positions
        self.fire_positions = {}  # fire_speed -> list of positions
        self.rows = 0
        self.cols = 0
        self.turn = 0
        self.move_limit = 100  # Default move limit
        
    def connect(self):
        """Connect to the server"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(30)
        self.sock.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")
        
    def receive_all(self, timeout=2) -> str:
        """Receive all available data"""
        self.sock.settimeout(timeout)
        data = b''
        try:
            while True:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                data += chunk
                # Small delay to allow more data to arrive
                time.sleep(0.01)
        except socket.timeout:
            pass
        return data.decode('utf-8', errors='ignore')
    
    def send(self, data: str):
        """Send data to server"""
        self.sock.sendall((data + '\n').encode())
        print(f"Sent: {data}")
        
    def decode_hex_row(self, hex_str: str) -> str:
        """Decode a hex-encoded row"""
        try:
            # Remove any whitespace
            hex_str = hex_str.strip()
            # Decode hex to bytes then to string
            decoded = binascii.unhexlify(hex_str)
            return decoded.decode('utf-8', errors='ignore')
        except:
            return hex_str  # Return as-is if decoding fails
    
    def parse_maze(self, maze_text: str):
        """Parse the maze from server output"""
        lines = maze_text.strip().split('\n')
        self.maze = []
        self.start_pos = None
        self.portals = {}
        self.fire_positions = {}
        self.turn = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try to decode as hex first
            decoded = self.decode_hex_row(line)
            
            # Check if it looks like a maze row (contains M, ., #, 1-3, a-e)
            if any(c in decoded for c in ['M', '.', '#', '1', '2', '3', 'a', 'b', 'c', 'd', 'e']):
                row = list(decoded)
                self.maze.append(row)
                
                for j, char in enumerate(row):
                    i = len(self.maze) - 1
                    if char == 'M':  # Player
                        self.start_pos = (i, j)
                    elif char in '123':  # Fire with speed
                        speed = int(char)
                        if speed not in self.fire_positions:
                            self.fire_positions[speed] = []
                        self.fire_positions[speed].append((i, j))
                    elif char in 'abcde':  # Portal
                        portal_id = char
                        if portal_id not in self.portals:
                            self.portals[portal_id] = []
                        self.portals[portal_id].append((i, j))
        
        self.rows = len(self.maze)
        self.cols = len(self.maze[0]) if self.maze else 0
        
    def get_char_at(self, pos: Tuple[int, int]) -> str:
        """Get character at position"""
        r, c = pos
        if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
            return '#'
        return self.maze[r][c]
    
    def is_valid_move(self, pos: Tuple[int, int], visited: Set[Tuple[int, int]], 
                     fire_positions: Set[Tuple[int, int]]) -> bool:
        """Check if a position is valid to move to"""
        r, c = pos
        if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
            return False
        if pos in visited:
            return False
        if pos in fire_positions:
            return False
        char = self.get_char_at(pos)
        # Can move through: empty space, player, portals, but not walls or fires
        if char == '#' or char in '123':
            return False
        return True
    
    def is_edge(self, pos: Tuple[int, int]) -> bool:
        """Check if position is on the edge of the maze"""
        r, c = pos
        return r == 0 or r == self.rows - 1 or c == 0 or c == self.cols - 1
    
    def get_portal_exit(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Get the other end of a portal if current position is a portal"""
        char = self.get_char_at(pos)
        if char in 'abcde':
            portal_id = char
            if portal_id in self.portals:
                portal_positions = self.portals[portal_id]
                for portal_pos in portal_positions:
                    if portal_pos != pos:
                        return portal_pos
        return None
    
    def simulate_fire_spread(self, turn: int) -> Set[Tuple[int, int]]:
        """Simulate fire spread up to given turn
        Fire speed K means it takes K turns to spread 1 cell.
        Multiple fires race - earliest arrival burns the cell.
        """
        # Track when each cell gets burned (turn number)
        burn_time = {}  # pos -> turn when burned
        
        # Initialize with starting fire positions (burned at turn 0)
        for speed, positions in self.fire_positions.items():
            for pos in positions:
                burn_time[pos] = 0
        
        # For each fire source, calculate how far it has spread by turn 'turn'
        for speed, positions in self.fire_positions.items():
            for fire_start in positions:
                # How many cells away can this fire reach by turn 'turn'?
                # Speed K means 1 cell per K turns, so at turn T, it's spread floor(T/K) cells
                max_distance = turn // speed if turn >= 0 else 0
                
                # BFS from fire source to find all cells within max_distance
                queue = deque([(fire_start, 0)])
                visited = set([fire_start])
                
                while queue:
                    fire_pos, distance = queue.popleft()
                    
                    if distance > max_distance:
                        continue
                    
                    # Calculate when this cell gets burned
                    # It takes (distance * speed) turns to reach this cell
                    burn_turn = distance * speed
                    
                    # Mark as burned at earliest time
                    if fire_pos not in burn_time or burn_time[fire_pos] > burn_turn:
                        burn_time[fire_pos] = burn_turn
                    
                    # Spread to neighbors
                    r, c = fire_pos
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        new_pos = (r + dr, c + dc)
                        if new_pos not in visited:
                            if self.get_char_at(new_pos) != '#':
                                visited.add(new_pos)
                                queue.append((new_pos, distance + 1))
        
        # Return all cells that are burned by the given turn
        return set(pos for pos, burn_t in burn_time.items() if burn_t <= turn)
    
    def bfs_escape(self, max_turns: int = None) -> Optional[List[str]]:
        """BFS to find shortest path to any edge, considering fire spread"""
        if not self.start_pos:
            return None
        
        if max_turns is None:
            max_turns = self.move_limit
        
        # Use state: (position, turn, path)
        queue = deque([(self.start_pos, 0, [])])
        visited = set([(self.start_pos, 0)])
        
        while queue:
            pos, turn, path = queue.popleft()
            
            # Check if we're on an edge
            if self.is_edge(pos):
                return path
            
            # Don't exceed move limit
            if turn >= max_turns:
                continue
            
            # Get fire positions at this turn
            fire_cells = self.simulate_fire_spread(turn)
            
            # Check if current position is a portal (use P to teleport)
            portal_exit = self.get_portal_exit(pos)
            if portal_exit and (portal_exit, turn) not in visited:
                # Portal costs 1 turn, so check fire at turn+1
                next_fire_cells = self.simulate_fire_spread(turn + 1)
                if self.is_valid_move(portal_exit, set(), next_fire_cells):
                    visited.add((portal_exit, turn + 1))
                    queue.append((portal_exit, turn + 1, path + ['P']))
            
            # Try regular moves (W=up, S=down, A=left, D=right)
            r, c = pos
            for dr, dc, direction in [(-1, 0, 'W'), (1, 0, 'S'), (0, -1, 'A'), (0, 1, 'D')]:
                new_pos = (r + dr, c + dc)
                new_turn = turn + 1
                state = (new_pos, new_turn)
                
                if state not in visited:
                    # Check fire at next turn - player must arrive before fire
                    next_fire_cells = self.simulate_fire_spread(new_turn)
                    # Also check if fire arrives at the same turn (player loses)
                    current_fire_cells = self.simulate_fire_spread(turn)
                    if self.is_valid_move(new_pos, set(), next_fire_cells) and new_pos not in current_fire_cells:
                        visited.add(state)
                        queue.append((new_pos, new_turn, path + [direction]))
        
        return None
    
    def solve_round_with_data(self, data: str, round_num: int) -> Optional[str]:
        """Solve one round with provided data"""
        print(f"\n=== Solving Round {round_num} ===")
        
        if not data:
            print("No data provided")
            return False
        """Solve one round of the maze"""
        print("\n=== New Round ===")
        
        print(f"Processing data length: {len(data)}")
        if len(data) > 0:
            print(f"First 1500 chars:\n{data[:1500]}")
        
        # Look for hex-encoded lines
        lines = data.split('\n')
        maze_lines = []
        
        # Extract move limit and start position from round data
        self.move_limit = 100  # Default
        round_start_pos = None
        
        # Find the round section
        in_round = False
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Check if we're in a round section
            if f'ROUND {round_num}' in line or (round_num == 1 and 'ROUND 1' in line):
                in_round = True
                continue
            
            # Extract LIMIT and START
            if in_round:
                if line_stripped.startswith('LIMIT'):
                    try:
                        self.move_limit = int(line_stripped.split()[1])
                        print(f"Move limit: {self.move_limit}")
                    except:
                        pass
                elif line_stripped.startswith('START'):
                    try:
                        parts = line_stripped.split()
                        round_start_pos = (int(parts[1]), int(parts[2]))
                        print(f"Start from data: {round_start_pos}")
                    except:
                        pass
            
            # Skip headers and separators
            if not in_round or not line_stripped:
                continue
            if '=' in line_stripped or 'ROUND' in line_stripped or 'GRID' in line_stripped or 'RULES' in line_stripped or 'SIZE' in line_stripped or 'START' in line_stripped or 'LIMIT' in line_stripped or 'PATH' in line_stripped:
                continue
            
            # Check if line looks like hex (even length, hex chars, reasonable length)
            if len(line_stripped) > 4 and all(c in '0123456789abcdefABCDEF' for c in line_stripped) and len(line_stripped) % 2 == 0:
                try:
                    decoded = self.decode_hex_row(line_stripped)
                    if any(c in decoded for c in ['M', '.', '#', '1', '2', '3', 'a', 'b', 'c', 'd', 'e']):
                        maze_lines.append(decoded)
                        if len(maze_lines) <= 5:  # Print first few
                            print(f"Decoded row {len(maze_lines)}: {decoded}")
                except Exception as e:
                    print(f"Error decoding line: {e}")
                    pass
        
        if not maze_lines:
            # Try parsing as plain text (in case it's not hex-encoded)
            in_round = False
            for line in lines:
                if f'ROUND {round_num}' in line or (round_num == 1 and 'ROUND 1' in line):
                    in_round = True
                    continue
                if in_round and line.strip() and any(c in line for c in ['M', '.', '#', '1', '2', '3', 'a', 'b', 'c', 'd', 'e']):
                    if '=' not in line and 'ROUND' not in line:
                        maze_lines.append(line.strip())
        
        if not maze_lines:
            print("Could not parse maze")
            print(f"Sample lines: {lines[:30]}")
            return None
        
        maze_text = '\n'.join(maze_lines)
        print(f"\nParsed maze ({len(maze_lines)} rows):")
        for i, row in enumerate(maze_lines[:10]):  # Print first 10 rows
            print(f"  {i}: {row}")
        if len(maze_lines) > 10:
            print(f"  ... ({len(maze_lines) - 10} more rows)")
        
        self.parse_maze(maze_text)
        
        # Use start position from parsing or from START line
        if not self.start_pos and round_start_pos:
            self.start_pos = round_start_pos
            print(f"Using start position from START line: {self.start_pos}")
        
        if not self.start_pos:
            print("Could not find start position")
            return False
        
        print(f"\nMaze info:")
        print(f"  Size: {self.rows}x{self.cols}")
        print(f"  Start: {self.start_pos}")
        print(f"  Portals: {self.portals}")
        print(f"  Fires: {self.fire_positions}")
        
        # Find path
        path = self.bfs_escape()
        
        if not path:
            print("No path found!")
            return None
        
        print(f"\nPath found ({len(path)} moves): {''.join(path[:50])}{'...' if len(path) > 50 else ''}")
        
        # Send full path as one line
        full_path = ''.join(path)
        self.send(full_path)
        
        # Wait for response
        time.sleep(0.5)
        response = self.receive_all(timeout=3)
        if response:
            print(f"Response: {response[:500]}")
        
        return response  # Return response for next round
    
    def solve(self):
        """Solve all rounds"""
        self.connect()
        
        # Initial greeting - receive everything
        time.sleep(0.5)
        initial = self.receive_all(timeout=3)
        print(f"Initial message length: {len(initial)}")
        print(f"Initial message:\n{initial[:2000]}")
        
        # Check if first round maze is already in initial data
        all_rounds_data = [initial]
        
        # Solve 5 rounds
        current_data = initial
        for round_num in range(1, 6):
            print(f"\n{'='*60}")
            print(f"ROUND {round_num}/5")
            print(f"{'='*60}")
            
            # Extract round data from current_data
            response_data = self.solve_round_with_data(current_data, round_num)
            if response_data is None:
                print(f"Failed on round {round_num}")
                break
            
            # Next round data should be in the response
            current_data = response_data
            # If response doesn't contain next round, try to receive more
            if f'ROUND {round_num + 1}' not in current_data and round_num < 5:
                time.sleep(0.5)
                additional_data = self.receive_all(timeout=3)
                if additional_data:
                    current_data += additional_data
        
        # Get final flag - receive any remaining data
        time.sleep(1)
        final = self.receive_all(timeout=3)
        print(f"\n{'='*60}")
        print("FINAL OUTPUT:")
        print(f"{'='*60}")
        print(final)
        
        self.sock.close()
    
    def solve_round(self) -> bool:
        """Solve one round - receives data from server"""
        data = self.receive_all(timeout=3)
        return self.solve_round_with_data(data, 1)

if __name__ == "__main__":
    solver = FireMazeSolver("chall.ehax.in", 31337)
    solver.solve()
```

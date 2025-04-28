# Solution

`.puz` file is an Across Lite crossword puzzle game. The solution in the puzzle is scrambled, need 4 digit key to unscramble and get the real solution. Bruteforce 4 digit key using python.

```
import sys
import puz
from puz import Puzzle, PuzzleFormatError
def brute_force_unlock(puz_file):
    """
    Attempt to brute-force unlock a scrambled .puz file by trying all possible 4-digit keys.
    """
    try:
        # Load the puzzle file
        puzzle = puz.read(puz_file)
        
        # Check if the puzzle is actually locked
        if not puzzle.is_solution_locked():
            print("Puzzle is not locked - no need to brute force")
            return True
        
        print(f"Attempting to brute force unlock {puz_file}")
        print(f"Puzzle title: {puzzle.title}")
        print(f"Dimensions: {puzzle.width}x{puzzle.height}")
        
        # Try all possible 4-digit keys (1000-9999)
        for key in range(1000, 10000):
            # Create a copy of the puzzle to test the key
            test_puzzle = Puzzle()
            test_puzzle.__dict__ = puzzle.__dict__.copy()
            
            # Try to unlock with this key
            if test_puzzle.unlock_solution(key):
                print(f"\nSuccess! Key found: {key}")
                
                # Save the unlocked puzzle
                output_file = f"unlocked_{key}_{puz_file}"
                test_puzzle.save(output_file)
                print(f"Unlocked puzzle saved as: {output_file}")
                
                # Print some puzzle info
                print("\nPuzzle info:")
                print(f"Title: {test_puzzle.title}")
                print(f"Author: {test_puzzle.author}")
                print(f"Copyright: {test_puzzle.copyright}")
                return True
            
            # Print progress every 100 keys
            if key % 100 == 0:
                print(f"Tried keys up to: {key}", end='\r')
        
        print("\nFailed to find the correct key (tried 1000-9999)")
        return False
    
    except PuzzleFormatError as e:
        print(f"Error reading puzzle file: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python puz_bruteforce.py <puzzle_file.puz>")
        sys.exit(1)
    
    puz_file = sys.argv[1]
    if not brute_force_unlock(puz_file):
        sys.exit(1)
```


Flag: `UMDCTF{CANYOUBEATMYTIME}`


Solved by: arifpeycal

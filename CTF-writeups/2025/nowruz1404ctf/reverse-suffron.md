# suffron
Solved by: @benkyou

### Question:
what time(stamp) is it?

### Solution:
Decompile `.pyc` with [https://pylingual.io/](https://pylingual.io/ "https://pylingual.io/") . Only the 1st permutation is taken so you can brute force the seed (assume small enough).

Solution code to parallelize:
```python
import random
import multiprocessing

# Function to shuffle and check for the flag
def try_flag(seed):
    flag = list('o1me0T3}h_hTuvar_M4vdCFF3__{l3TY')
    random.seed(seed)
    random.shuffle(flag)
    flagstr = ''.join(flag)
    if 'FMCTF{' in flagstr:
        return flagstr
    return None

# Function to divide the work and search in parallel
def parallel_search(start_seed, num_processes, range_size):
    # Create a pool of worker processes
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Distribute seed ranges for each process
        results = pool.map(try_flag, range(start_seed, start_seed - range_size, -1))
        
        # Look for the first non-None result (flag)
        for result in results:
            if result:
                print(f"Found flag: {result}")
                return result
    return None

if __name__ == '__main__':
    start_seed = 1742050000  # The starting seed value
    num_processes = 4  # Number of parallel processes
    range_size = 1000000  # How many seeds each process will handle (adjust as needed)

    # Run the parallel search with a large range
    flag = parallel_search(start_seed, num_processes, range_size)
    
    # If flag is found, print it
    if flag:
        print(f"Flag found: {flag}")
    else:
        print("Flag not found in the given range.")
```

**Flag:** `FMCTF{0h_You_h4v3_Trav3led_T1m3}`

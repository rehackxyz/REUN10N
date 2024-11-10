# HMAC

Solved by: @vicevirus

## Question:
There’s a secret message being HMAC-protected, but the implementation has a serious flaw. Can you recover the secret message using a side-channel attack?

SRC: https://gist.github.com/AndyNovo/91e3c51ef47980d32ad1cde26b917ac4

## Solution:

```
from pwn import *
import time
import logging

# Configuration
HOST = '0.cloud.chals.io'
PORT = 11320
TIMEOUT = 1
LOG_FILE = "attack_log.txt"

# Initialize logging to a file
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger()  # Use the same log object for all logs

def connect():
    """Establish a connection to the remote server, retrying until successful."""
    while True:
        try:
            r = remote(HOST, PORT, timeout=TIMEOUT)
            log.info("Connection established.")
            return r
        except Exception as e:
            log.error(f"Failed to connect: {e}. Retrying...")
            time.sleep(1)

def send_guess(guess_hex):
    """Send the hex-encoded guess to the server and measure the response time, retrying on failure."""
    while True:
        r = connect()
        try:
            start = time.perf_counter()
            r.sendlineafter(b'>', guess_hex)
            response = r.recvline(timeout=TIMEOUT)
            end = time.perf_counter()
            elapsed = end - start
            return elapsed, response
        except EOFError:
            log.error("Connection closed by the server. Retrying...")
            time.sleep(1)
        except Exception as e:
            log.error(f"Error during communication: {e}. Retrying...")
            time.sleep(1)
        finally:
            r.close()

def guess_byte(guess, byte_idx, recovered):
    """Attempt to guess a single byte and return the elapsed time taken."""
    guess_byte = bytes([guess])
    guess_hmac = recovered + guess_byte
    guess_hmac_padded = guess_hmac.ljust(6, b'\x00')
    guess_hex = guess_hmac_padded.hex().encode()

    elapsed, response = send_guess(guess_hex)
    return guess, elapsed

def find_consistent_byte(byte_idx, recovered_hmac):
    """Repeat the process for each byte until a consistent byte is found in 3 out of 6 attempts."""
    while True:
        attempts = []
        for attempt in range(6):  # Increase attempts to 6
            # Collect timing data for each possible byte
            timings = {}
            log.info(f"Attempt {attempt + 1} to recover byte {byte_idx + 1}")

            for guess in range(256):
                guess_val, elapsed_time = guess_byte(guess, byte_idx, recovered_hmac)
                timings[guess_val] = elapsed_time
                log.debug(f"Byte {byte_idx + 1}: Guess {guess_val:02x} Time: {elapsed_time:.4f}s")

            # Select the byte with the maximum timing, indicating the likely correct byte
            best_guess = max(timings, key=timings.get)
            best_time = timings[best_guess]
            log.info(f"Attempt result for byte {byte_idx + 1}: Guess {best_guess:02x} (Time: {best_time:.4f}s)")
            attempts.append(best_guess)

        # Check if the same byte was guessed 3 out of 6 times
        most_common_guess = max(set(attempts), key=attempts.count)
        if attempts.count(most_common_guess) >= 3:
            log.info(f"Confirmed byte {byte_idx + 1}: {most_common_guess:02x}")
            return most_common_guess
        else:
            log.warning(f"Inconsistent results for byte {byte_idx + 1}. Retrying...")

def recover_hmac():
    """Recover each byte of the HMAC by timing comparisons with consistency checking."""
    recovered_hmac = b""  # Start without any pre-set bytes

    for byte_idx in range(6):  # Recover each byte from scratch
        consistent_byte = find_consistent_byte(byte_idx, recovered_hmac)
        recovered_hmac += bytes([consistent_byte])

    return recovered_hmac

def main():
    log.info("Starting timing attack to recover HMAC...")
    recovered_hmac = recover_hmac()
    log.info(f"Recovered HMAC (first 6 bytes): {recovered_hmac.hex()}")

    # Now, send the recovered HMAC to get the flag
... (17 lines left)
          ```
Visit https://bluehens-webstuff.chals.io/flagme.php?password=1qaz2wsx
**Flag:`UDCTF{B4d_T1miN6}`** 

# Solution
```
import sys
from web3 import Web3

# --- CONFIGURATION ---
RPC_URL = "http://public.ctf.r0devnull.team:3011/25c82439-76cb-4707-8b9f-83560fde2ef4"
SETUP_ADDR = "0xC8Ea544D608594e762146770c0D0F53a2d5039c2"

# --- CHECK LOGIC ---
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    print("Error: Failed to connect to RPC.")
    sys.exit(1)

# Interface to check isSolved
setup_abi = [
    {"inputs": [], "name": "isSolved", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "casino", "outputs": [{"internalType": "contract Casino", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}
]
setup_contract = w3.eth.contract(address=SETUP_ADDR, abi=setup_abi)

# Get status
try:
    solved = setup_contract.functions.isSolved().call()
    casino_addr = setup_contract.functions.casino().call()
    
    # Check Casino Balance (Optional, to see how much is left)
    # The Setup contract says it is solved when token balance < 1 ether, 
    # but usually we drain the ETH liquidity. 
    # Let's check the ETH balance of the Casino just in case.
    casino_balance = w3.from_wei(w3.eth.get_balance(casino_addr), 'ether')

    print(f"\n[*] Target Casino: {casino_addr}")
    print(f"[*] Casino ETH Balance: {casino_balance} ETH")
    print(f"[*] Challenge Solved? : {solved}")

    if solved:
        print("\n[!!!] CONGRATULATIONS! FLAG CAPTURED [!!!]")
    else:
        print("\n[!] Not solved yet. You need to restart the attack.py script.")

except Exception as e:
    print(f"Error checking status: {e}")
```
Flag:nullctf{w!nn!ng_is_s0_much_fun!!}

Solved by: ha1qal

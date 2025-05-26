# Solution

Check the boxes 20k (can change) at a time using js. After it hit 2 mil, refresh and get flag  

```
(() => {
  const host = window.location.host;
  const TOTAL  = 2_000_000;
  const BATCH  = 20_000;
  let start = 0;

  const ws = new WebSocket(`ws://${host}/ws`);
  ws.onopen = () => {
    ws.send(JSON.stringify({ action: 'get_state' }));

    function sendBatch() {
      if (start >= TOTAL) return;
      const end = Math.min(start + BATCH, TOTAL);
      // build [start, start+1, …, end-1]
      const nums = Array.from({length: end - start}, (_, i) => start + i);
      ws.send(JSON.stringify({ action: 'check', numbers: nums }));
      start = end;
      setTimeout(sendBatch, 50);
    }
    sendBatch();
  };

  ws.onmessage = (evt) => {
    console.log('→', evt.data);
  };
})();

```

Flag:`flag{7d798903eb2a1823803a243dde6e9d5b}`

Solved by: zeqzoq

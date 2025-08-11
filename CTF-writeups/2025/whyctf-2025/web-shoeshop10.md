## Description
We created a new [shoe shop](https://shoe-shop-1.ctf.zone/), so we can sell some shoes. Too bad the admin already put the exclusive shoe in his shopping cart, but feel free to browse around and check out if there are some shoes you like

## Solution
IDOR in the cart page (you need to be authenticated).
<https://shoe-shop-1.ctf.zone/index.php?page=cart&id=1>

Flag: `flag{00f34f9c417fcaa72b16f79d02d33099}`


Solved by: benkyou
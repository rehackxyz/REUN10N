# Solution

We discover a source map file exposed at:
https://web-mini-me-ab6d19a7ea6e.2025.ductf.net/static/js/test-main.min.js.map
This reveals the original JavaScript source under `sourcesContent`

Inside the de-obfuscated source is this function:
```
function qyrbkc() {
    const xtqzp = ["85"], vmsdj = ["87"], rlfka = ["77"], wfthn = ["67"], zdqo = ["40"], yclur = ["82"],
          bpxmg = ["82"], hkfav = ["70"], oqzdu = ["78"], nwtjb = ["39"], sgfyk = ["95"], utxzr = ["89"],
          jvmqa = ["67"], dpwls = ["73"], xaogc = ["34"], eqhvt = ["68"], mfzoj = ["68"], lbknc = ["92"],
          zpeds = ["84"], cvnuy = ["57"], ktwfa = ["70"], xdglo = ["87"], fjyhr = ["95"], vtuze = ["77"], awphs = ["75"];
          
    const dhgyvu = [xtqzp[0], vmsdj[0], rlfka[0], wfthn[0], zdqo[0], yclur[0], 
                    bpxmg[0], hkfav[0], oqzdu[0], nwtjb[0], sgfyk[0], utxzr[0], 
                    jvmqa[0], dpwls[0], xaogc[0], eqhvt[0], mfzoj[0], lbknc[0], 
                    zpeds[0], cvnuy[0], ktwfa[0], xdglo[0], fjyhr[0], vtuze[0], awphs[0]];
​
    const lmsvdt = dhgyvu.map((pjgrx, fkhzu) =>
        String.fromCharCode(
            Number(pjgrx) ^ (fkhzu + 1)
        )
    ).reduce((qdmfo, lxzhs) => qdmfo + lxzhs, "");
}


```

Decode with python3
```
dhgyvu = [85, 87, 77, 67, 40, 82, 82, 70, 78, 39,
          95, 89, 67, 73, 34, 68, 68, 92, 84, 57,
          70, 87, 95, 77, 75]

key = ''.join(chr(num ^ (i + 1)) for i, num in enumerate(dhgyvu))
print(key)

```
Output: TUNG-TUNG-TUNG-TUNG-SAHUR

curl -X POST https://web-mini-me-ab6d19a7ea6e.2025.ductf.net/admin/flag \
  -H "X-API-Key: TUNG-TUNG-TUNG-TUNG-SAHUR"

Flag: DUCTF{Cl13nt-S1d3-H4ck1nG-1s-FuN}


Solved by: asyraf16
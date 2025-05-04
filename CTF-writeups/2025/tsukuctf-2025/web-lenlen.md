```javascript
function chall(str = "[1, 2, 3]") {
  const sanitized = str.replaceAll(" ", "");
  if (sanitized.length < 10) {
    return `error: no flag for you. sanitized string is ${sanitized}, length is ${sanitized.length.toString()}`;
  }
  const array = JSON.parse(sanitized);
  if (array.length < 0) {
    // hmm...??
    return FLAG;
  }
  return `error: no flag for you. array length is too long -> ${array.length}`;
}
```
The bug here is because array is created from `JSON.parse()`, so we can parse a JSON object with length=-1 to pass the `sanitized.length < 10`  and `array.length < 0` checks.

```
curl http://challs.tsukuctf.org:28888 -X POST -d 'array={"length": -1}'
TsukuCTF25{l4n_l1n_lun_l4n_l0n}
```

Solved by: benkyou
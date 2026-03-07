# web - borderline personality

Solved by: p5yd4wk

In this challenge, the web use HAProxy and flask backend on different port. HAProxy blocks access to /admin paths

vulnerability: HAProxy misconfiguration, HAProxy performs path matching before URL encoding while the flask backend decodes the URL before routing. This create a slight mistmatch for us to exploit

simple inject http://chall.ehax.in:9098/%2fadmin/flag to bypass. This works because HAProxy cant process `%2` while the backend can
flag: `EH4X{BYP4SSING_R3QU3S7S_7HR0UGH_SMUGGLING__IS_H4RD}`

Solved by: yappare
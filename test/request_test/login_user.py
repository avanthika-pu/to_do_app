import requests

url = "http://127.0.0.1:5000/auth/login"

data = {
    "email": "abcd@gmail.com",
    "password": "ABCD@123"
}

response = requests.post(url, json=data)

print(response.status_code)  
print(response.json())

import requests

url = "http://127.0.0.1:5000/auth/register"

data = {
    "email": "rahul@gmail.com",
    "password": "Rahul@123",
    "first_name": "Rahul",
    "last_name": "S"
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())

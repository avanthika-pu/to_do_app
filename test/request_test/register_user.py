import requests

url = "http://127.0.0.1:5000/auth/register"

data = {
    "email": "krish@example.com",
    "password": "Krish@123",
    "first_name": "Krish",
    "last_name": "K"
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())

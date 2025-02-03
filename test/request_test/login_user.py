import requests

url = "http://127.0.0.1:5000/auth/login"  

data = {
    "email": "krish@example.com",
    "password": "Krish@123"
}

response = requests.post(url, json=data)

print(response.status_code) 
print(response.text)      
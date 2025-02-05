
import requests

url = "http://127.0.0.1:5000/auth/login"  

data = {
    "email": "anjima@gmail.com",
    "password": "Anjima@123"
}
response = requests.post(url, json=data)

print(response.status_code) 
print(response.text)
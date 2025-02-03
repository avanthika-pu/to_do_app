import requests

url = "http://127.0.0.1:5000/auth/register"  
data = {
    "first_name": "marco",
    "last_name": "J",
    "email": "marco@gmail.com",
    "password": "Marco@123"
}

response = requests.post(url, json=data)

print(response.status_code) 
print(response.text)      

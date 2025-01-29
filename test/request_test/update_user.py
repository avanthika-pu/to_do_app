import requests

url = 'http://localhost:5000/user/update/1'

data = {
    "email": "david@gmail.com",
    "first_name": "David",
    "last_name": "Vj",
    "password": "David123"
}

response = requests.put(url, json=data)

print(response.status_code)
print(response.text)

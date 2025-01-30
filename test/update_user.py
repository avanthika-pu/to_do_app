import requests

user_id = 1 
url = f"http://127.0.0.1:5000/user/update/{user_id}"

user_data = {
    "name": "Mathew",
    "email": "mathewfernandes@email.com"
}

response = requests.put(url, json=user_data)

print(response.status_code)
print(response.text)
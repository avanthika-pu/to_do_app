import requests

url = 'http://127.0.0.1:5000/user/create'

form_data = {
                'email': 'maya@gmail.com',
                'first_name': 'Maya',
                'last_name': 'John',
                'password':'Maya@123'
}

response = requests.post(url,json=form_data)
print(response.status_code)
print(response.json)
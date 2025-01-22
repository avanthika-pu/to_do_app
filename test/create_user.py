import requests

url = 'http://127.0.0.1:5001/user/create'

form_data = {
                'email': 'Johndoe@gmail.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'password':'John@123'
}

response = requests.post(url,json=form_data)
print(response.status_code)
print(response.json)
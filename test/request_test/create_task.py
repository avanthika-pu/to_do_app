import requests

url = 'http://127.0.0.1:5000/task/create' 

task_data = {
    'title': 'Day today activity',
    'description': 'Days workouts',
    'user_id': 1
}

response = requests.post(url, json=task_data)  
print(response.status_code)
print(response.json)

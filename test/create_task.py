import requests

url = 'http://127.0.0.1:5001/task/tasks' 

task_data = {
    'title': 'To_Do_App',
    'description': 'Day activity',
    'user_id': 1
}

response = requests.post(url, json=task_data)  
print(response.status_code)
print(response.text)

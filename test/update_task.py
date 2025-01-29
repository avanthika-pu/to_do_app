import requests

url = "http://127.0.0.1:5000/task/update/1" 

task_data = {
    "title": "Updated Task Title",
    "description": "Updated Task Description"
}


response = requests.put(url, json=task_data)


print(response.status_code)  
print(response.json())  

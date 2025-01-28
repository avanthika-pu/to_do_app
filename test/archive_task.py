import requests

task_id = 1 
url = f"http://127.0.0.1:5000/task/archive/{task_id}"

response = requests.put(url)

print(response.status_code) 
print(response.text) 
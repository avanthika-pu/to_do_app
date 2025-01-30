import requests

url = "http://127.0.0.1:5001/task/delete_task/1"

task_id = 1

response = requests.delete(url)
print(response.status_code)

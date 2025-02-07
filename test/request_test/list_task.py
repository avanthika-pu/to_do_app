import requests

url = 'http://localhost:5000/task/task'  
response = requests.get(url)

response = requests.get(url)
print(response.status_code)
print(response.text)  


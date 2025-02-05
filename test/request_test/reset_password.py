import requests


url = "http://127.0.0.1:5000/auth/reset_password"  


auth_token = ".eJyrVspMUbIystBRSsssKi6Jz0vMTVWyUgpKzCjNUdJRyklEiAUD-am5iZk5QHYRSN4hHcTTS87PVaoFAERIF34.Z6IB1Q.FleqoRFQn0AjVGZuNWv99di_apI"

payload = {
    "new_password": "aminew@123",
    "confirm_password": "aminew@123",
}


headers = {
    "Content-Type": "application/json",
    "Authorization": f"Token {auth_token}"
}


response = requests.patch(url, json=payload, headers=headers)

print(response.status_code)
print(response.text)

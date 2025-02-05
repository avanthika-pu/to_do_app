import requests


url = "http://127.0.0.1:5000/auth/logout"

auth_token = ".eJyrVspMUbIystRRSsssKi6Jz0vMTVWyUnLMy8rMTVTSUcpJRAj6AvmpuYmZOUB2IliBQzqIq5ecn6tUCwBzGBgh.Z6MGqg.LyDzcPQ_LApkgSRLY0F5XIru6oE"
headers = {
    "Authorization": f"Token {auth_token}"
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)

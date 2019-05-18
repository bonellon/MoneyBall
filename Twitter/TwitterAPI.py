import requests
import json

endpoint = "https://api.twitter.com/1.1/tweets/search/fullarchive/main.json"

headers = {"Authorization":"Bearer AAAAAAAAAAAAAAAAAAAAAOj2%2BQAAAAAAQUuNtoCEgrb9lAEfoZHP9EpGsYc%3DaXiehoNql3kYAJ5j1Bn3rojl2CTwpJB9uhfCbbxZ8l2gQzUJpR", "Content-Type": "application/json"}

data = '{"query":"#fpl", "fromDate": "201802020000", "toDate": "201802240000"}'

response = requests.post(endpoint,data=data,headers=headers).json()

print(json.dumps(response, indent = 2))
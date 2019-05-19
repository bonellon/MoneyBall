import requests
import json

endpoint = "https://api.twitter.com/1.1/tweets/search/fullarchive/main.json"
bearer = "AAAAAAAAAAAAAAAAAAAAAOj2%2BQAAAAAAQUuNtoCEgrb9lAEfoZHP9EpGsYc%3DaXiehoNql3kYAJ5j1Bn3rojl2CTwpJB9uhfCbbxZ8l2gQzUJpR"

currentGW = 4
gwString = "gw"+str(currentGW)

midnight = "0000"


headers = {"Authorization":"Bearer "+bearer, "Content-Type": "application/json"}
data = '{"query":"in out #fpl #'+gwString+'", "fromDate": "20180827'+midnight+'", "toDate": "20180901'+midnight+'"}'

response = requests.post(endpoint, data=data, headers=headers).json()

with open('GW_Tweets/'+gwString+'.json', 'w') as outFile:
    json.dump(response, outFile)


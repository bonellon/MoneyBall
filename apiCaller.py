import requests

i = 2
models = ["gbm", "rf"]

for i in range(17,39):
    for model in models:
        url = 'http://127.0.0.1:5000/predict/'+str(i)+'/'+model

        print("Awaiting response for model = "+model+"\n GW = "+str(i))
        response = requests.get(url)
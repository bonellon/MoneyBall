import json
import random
from WEB import Formation

def getRand(models):
    rand = random.randint(0, 1)

    value = models[0]
    if rand == 0:
        value = models[1]
    return value

def generateRandomValue(model, data):

    models = ["svm", "rf", "gbm"]
    models.remove(model)

    value = getRand(models)

    goalkeepers = data[value]["goalkeepers"][0]

    defenders = []
    for i in range(0, 4):
        value = getRand(models)
        if data[value]['defenders'][i] not in defenders:
            defenders.append(data[value]['defenders'][i])
        else:
            i = i-1

    midfielders = []
    for i in range(0, 5):
        value = getRand(models)
        if data[value]['midfielders'][i] not in midfielders:
            midfielders.append(data[value]['midfielders'][i])
        else:
            i = i-1

    forwards = []
    for i in range(0, 1):
        value = getRand(models)

        if data[value]['forwards'][i] not in forwards:
            forwards.append(data[value]['forwards'][i])
        else:
            i = i-1

    newModel = Formation.Model(model, goalkeepers, defenders, midfielders, forwards).__dict__
    return newModel


with open("WEB/gameweeks.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

del data['1']

for gw in data:
    for model in data[gw]:

        if model == "gameweek":
            continue

        current = data[gw][model]

        if current["goalkeepers"] == []:
            print(model, data[gw]["gameweek"])
            data[gw][model] = generateRandomValue(model, data[gw])

with open('WEB/gameweeks.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
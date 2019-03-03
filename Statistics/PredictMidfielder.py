import csv
import Statistics.PredictMain as predict

required = predict.required

def getMidfielders():
    print("----getMidfielders")
    midfielders = {}
    with open('stats/midfielders.csv', 'r', newline='') as fp:
        reader = csv.DictReader(fp, dialect='excel')
        for row in reader:
            id = row['id']
            midfielders[id] = row
    return midfielders

def getPlayerScore(player):
    threat = float(player['threat'])
    form = float(player['form'])

    ep_next = float(player['ep_next'])
    cost = float(player['now_cost'])

    totalScore = ((ep_next + (form * threat))/(cost/100))/1000
    player['predictedValue'] = totalScore
    return float(totalScore)


def PredictMidfielders():
    print("--PredictMidfielders")
    midfielders = getMidfielders()

    top = []
    for midfielderID in midfielders:
        midfielder = midfielders[midfielderID]
        if len(top) < required:
            top.append(midfielder)

        else:
            isSorted = False
            while not isSorted:
                # order first REQUIRED elements
                changeMade = False
                for i in range(1, len(top) - 1):

                    current = top[i]
                    prev = top[i - 1]

                    if getPlayerScore(current) > getPlayerScore(prev):
                        changeMade = True
                        temp = current
                        top[i] = prev
                        top[i - 1] = temp

                if not changeMade:
                    isSorted = True

            #Update rest
            insertAtPosition = required - 1
            updated = False
            for i in range (0, len(top)-1):
                current = top[i]
                if getPlayerScore(current) < getPlayerScore(midfielder):
                    insertAtPosition = i
                    updated = True
                    break

            if updated:
                temp = top[insertAtPosition]
                top[insertAtPosition] = midfielder

                if insertAtPosition < required - 1:
                    for i in range(insertAtPosition + 1, len(top) - 1):
                        temp2 = top[i]
                        top[i] = temp
                        temp = temp2

    for player in top:
        player['predictedValue'] = getPlayerScore(player)
    return predict.sortAndRemove(top)
import csv
import Statistics.PredictMain as predict

required = predict.required

def getDefenders():
    print("----getDefenders")
    defenders = {}
    with open('stats/defenders.csv', 'r', newline='') as fp:
        reader = csv.DictReader(fp, dialect='excel')
        for row in reader:
            id = row['id']
            defenders[id] = row
    return defenders


def getPlayerScore(player):
    threat = float(player['threat'])
    form = float(player['form'])
    cost = float(player['now_cost'])
    cleansheets = int(player['clean_sheets'])
    conceded = int(player['goals_conceded'])

    ep_next = float(player['ep_next'])

    if conceded > 0:
        totalScore = (ep_next * form) + (cleansheets / conceded)
    else:
        totalScore = (ep_next * form) + cleansheets
    totalScore = (totalScore/cost)
    player['predictedValue'] = totalScore
    return float(totalScore)

def getPlayerScore(player):
    totalScore = 0;

    threat = float(player['threat'])
    form = float(player['form'])

    ep_next = float(player['ep_next'])

    totalScore = ep_next + (form * threat)
    player['predictedValue'] = totalScore
    return float(totalScore)


def PredictDefenders():
    print("--PredictDefenders")
    defenders = getDefenders()

    top = []
    for defenderID in defenders:
        defender = defenders[defenderID]
        if len(top) < required:
            top.append(defender)

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

            # Update rest
            insertAtPosition = required - 1
            updated = False
            for i in range(0, len(top) - 1):
                current = top[i]
                if getPlayerScore(current) < getPlayerScore(defender):
                    insertAtPosition = i
                    updated = True
                    break

            if updated:
                temp = top[insertAtPosition]
                top[insertAtPosition] = defender

                if insertAtPosition < required - 1:
                    for i in range(insertAtPosition + 1, len(top) - 1):
                        temp2 = top[i]
                        top[i] = temp
                        temp = temp2

    for player in top:
        player['predictedValue'] = getPlayerScore(player)
    return predict.sortAndRemove(top)

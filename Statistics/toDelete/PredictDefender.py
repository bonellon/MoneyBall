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
    form = float(player['form'])
    cost = float(player['now_cost'])
    cleansheets = int(player['clean_sheets'])
    conceded = int(player['goals_conceded'])

    ep_next = float(player['ep_next'])
    transfer_ratio = float(player['transfers_in_event']) / float(player['transfers_out_event'])
    player['transferRatio'] = transfer_ratio
    if conceded > 0:
        totalScore = (ep_next * form) * (cleansheets / conceded)
    else:
        totalScore = (ep_next * form) * cleansheets
    totalScore = (totalScore/cost)*transfer_ratio/cost
    player['predictedValue'] = totalScore
    return float(totalScore)

def PredictDefenders():
    print("--PredictDefenders")
    defenders = getDefenders()

    playersList = []
    for key, value in defenders.items():
        playersList.append([key, value])

    top = predict.sortList(playersList[0:required])
    for playerTup in playersList[required:]:
        player = playerTup[1]

        # Update rest
        insertAtPosition = required
        updated = False

        for i in range(0, len(top)):
            current = top[i]
            if getPlayerScore(current[1]) < getPlayerScore(player):
                insertAtPosition = i
                updated = True
                break

        if updated:
            top[insertAtPosition] = playerTup
            top = predict.sortList(top)


    for playerTup in top:
        player = playerTup[1]
        player['predictedValue'] = getPlayerScore(player)

#    predict.getTopTransfers(defenders)
    return predict.sortAndRemove(top)

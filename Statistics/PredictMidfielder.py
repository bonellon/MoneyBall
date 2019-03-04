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

    transfer_in = float(player['transfers_in_event'])
    transfer_out = float(player['transfers_out_event'])
    transfer_ratio = 0.1
    if transfer_in > 0.0 and transfer_out > 0.0:
        transfer_ratio = transfer_in / transfer_out
    player['transferRatio'] = transfer_ratio

    totalScore = ((ep_next + (form * threat)) / cost) / 10000
    totalScore = totalScore*transfer_ratio
    player['predictedValue'] = totalScore
    return float(totalScore)


def PredictMidfielders():
    print("--PredictMidfielders")
    midfielders = getMidfielders()

    playersList = []
    for key, value in midfielders.items():
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

#    predict.getTopTransfers(midfielders)
    return predict.sortAndRemove(top)
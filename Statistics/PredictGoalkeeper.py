import csv
import Statistics.PredictMain as predict

required = predict.required

def getGoalkeepers():
    print("----getGoalkeepers")
    goalkeepers = {}
    with open('stats/goalkeepers.csv', 'r', newline='') as fp:
        reader = csv.DictReader(fp, dialect='excel')
        for row in reader:
            id = row['id']
            goalkeepers[id] = row
    return goalkeepers

def getPlayerScore(player):
    predict.getTransferCounts(player)
    cleansheets = int(player['clean_sheets'])
    conceded = int(player['goals_conceded'])

    form = float(player['form'])

    ep_next = float(player['ep_next'])
    transfer_ratio = float(player['transfers_in_event']) / float(player['transfers_out_event'])
    player['transferRatio'] = transfer_ratio

    if conceded > 0:
        totalScore = ep_next + (form / 100) + (cleansheets / conceded)
    else:
        totalScore = ep_next + (form / 100) + cleansheets
    totalScore = totalScore*transfer_ratio
    player['predictedValue'] = totalScore
    return float(totalScore)


def PredictGoalkeepers():
    print("--PredictGoalkeepers")
    goalkeepers = getGoalkeepers()

    playersList = []
    for key, value in goalkeepers.items():
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

    #predict.getTopTransfers(goalkeepers)
    return predict.sortAndRemove(top)

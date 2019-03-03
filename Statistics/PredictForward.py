import csv
import Statistics.PredictMain as predict

required = predict.required


def getForwards():
    print("----getForwards")
    forwards = {}
    with open('stats/forwards.csv', 'r', newline='') as fp:
        reader = csv.DictReader(fp, dialect='excel')
        for row in reader:
            id = row['id']
            forwards[id] = row
    return forwards


# getPlayerScore finds top 5 players and 1 random -> sorts and removes last element
# hack -> temp solution
def sortAndRemove(top):
    print("----sortAndRemove")
    currentTop = {}
    for i in range(0, len(top)):
        currentTop[i] = top[i]

    sortedTop = sorted(currentTop.items(), key=lambda v: v[1]['ep_next'])
    return sortedTop


def getPlayerScore(player):

    threat = float(player['threat'])
    form = float(player['form'])

    ep_next = float(player['ep_next'])

    totalScore = ep_next + (form * threat)
    player['predictedValue'] = totalScore
    return float(totalScore)


def PredictForwards():
    print("--PredictForwards")
    forwards = getForwards()

    playersList = []
    for key, value in forwards.items():
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

    predict.getTopTransfers(forwards)
    return predict.sortAndRemove(top)

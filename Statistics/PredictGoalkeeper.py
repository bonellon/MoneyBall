import csv

required = 6

def getGoalkeepers():
    print("----getGoalkeepers")
    goalkeepers = {}
    with open('stats/goalkeepers.csv', 'r', newline='') as fp:
        reader = csv.DictReader(fp, dialect='excel')
        for row in reader:
            id = row['id']
            goalkeepers[id] = row
    return goalkeepers


# getPlayerScore finds top 5 players and 1 random -> sorts and removes last element
# hack -> temp solution
def sortAndRemove(top):
    currentTop = {}
    for i in range(0, len(top)):
        currentTop[i] = top[i]

    sortedTop = sorted(currentTop.items(), key=lambda v: v[1]['ep_next'])
    return sortedTop[1:]


def getPlayerScore(player):
    totalScore = 0;

    cleansheets = int(player['clean_sheets'])
    conceded = int(player['goals_conceded'])

    form = float(player['form'])

    ep_next = float(player['ep_next'])


    if conceded > 0:
        totalScore = ep_next + (form / 100) + cleansheets / conceded
    else:
        totalScore = ep_next + (form / 100)

    player['predictedValue'] = totalScore
    return float(totalScore)


def PredictGoalkeepers():
    print("--PredictGoalkeepers")
    goalkeepers = getGoalkeepers()

    top = []
    for goalkeeperID in goalkeepers:
        goalkeeper = goalkeepers[goalkeeperID]
        if len(top) < required:
            top.append(goalkeeper)

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
                if getPlayerScore(current) < getPlayerScore(goalkeeper):
                    insertAtPosition = i
                    updated = True
                    break

            if updated:
                temp = top[insertAtPosition]
                top[insertAtPosition] = goalkeeper

                if insertAtPosition < required - 1:
                    for i in range(insertAtPosition + 1, len(top) - 1):
                        temp2 = top[i]
                        top[i] = temp
                        temp = temp2


    for player in top:
        player['predictedValue'] = getPlayerScore(player)
    return sortAndRemove(top)
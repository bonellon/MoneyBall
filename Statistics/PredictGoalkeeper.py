import csv

required = 6

def getGoalkeepers():
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


def PredictGoalkeepers():

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

                    if (current['ep_next'] > prev['ep_next']):
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
                if current['ep_next'] < goalkeeper['ep_next']:
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

    return sortAndRemove(top)
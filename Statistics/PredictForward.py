import csv
import collections

required = 6


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
    currentTop = {}
    for i in range(0, len(top)):
        currentTop[i] = top[i]

    sortedTop = sorted(currentTop.items(), key=lambda v: v[1]['ep_next'])
    return sortedTop[1:]


def getPlayerScore(player):
    totalScore = 0;

    threat = float(player['threat'])
    form = float(player['form'])

    ep_next = float(player['ep_next'])

    totalScore = ep_next + (form * threat)
    player['predictedValue'] = totalScore
    # return float(totalScore)
    return float(ep_next)


def PredictForwards():
    print("--PredictForwards")
    forwards = getForwards()

    top = []
    for forwardID in forwards:
        forward = forwards[forwardID]
        if len(top) < required:
            top.append(forward)

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
                if getPlayerScore(current) < getPlayerScore(forward):
                    insertAtPosition = i
                    updated = True
                    break

            if updated:
                temp = top[insertAtPosition]
                top[insertAtPosition] = forward

                if insertAtPosition < required - 1:
                    for i in range(insertAtPosition + 1, len(top) - 1):
                        temp2 = top[i]
                        top[i] = temp
                        temp = temp2

    return sortAndRemove(top)

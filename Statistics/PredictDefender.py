import csv

def getDefenders():
    defenders = {}
    with open('stats/defenders.csv', 'r', newline='') as fp:
        reader = csv.DictReader(fp, dialect='excel')
        for row in reader:
            id = row['id']
            defenders[id] = row
    return defenders

def PredictDefenders(defenders):
    top5 = []
    for defenderID in defenders:
        defender = defenders[defenderID]
        if len(top5) < 5:
            top5.append(defender)

        else:
            isSorted = False
            while not isSorted:
                # order first 5 elements
                changeMade = False
                for i in range(1, len(top5) - 1):

                    current = top5[i]
                    prev = top5[i - 1]

                    if (current['ep_next'] > prev['ep_next']):
                        changeMade = True
                        temp = current
                        top5[i] = prev
                        top5[i - 1] = temp

                if not changeMade:
                    isSorted = True

            #Update rest
            insertAtPosition = 4
            updated = False
            for i in range (0, len(top5)-1):
                current = top5[i]
                if current['ep_next'] < defender['ep_next']:
                    insertAtPosition = i
                    updated = True
                    break

            if updated:
                temp = top5[insertAtPosition]
                top5[insertAtPosition] = defender

                if insertAtPosition < 4:
                    for i in range(insertAtPosition + 1, len(top5) - 1):
                        temp2 = top5[i]
                        top5[i] = temp
                        temp = temp2


    return top5
import csv

required = 5


def getMidfielders():
    midfielders = {}
    with open('stats/midfielders.csv', 'r', newline='') as fp:
        reader = csv.DictReader(fp, dialect='excel')
        for row in reader:
            id = row['id']
            midfielders[id] = row
    return midfielders

def PredictMidfielders():

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
                if current['ep_next'] < midfielder['ep_next']:
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


    return top
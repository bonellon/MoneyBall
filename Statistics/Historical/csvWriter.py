import csv
from collections import OrderedDict

'''
Player
    1
        isCaptain
        opponent_NextWeek
        opponent_team       -> change to opponent
        player
        points_NextWeek
        round
        total_points        -> change to points
    2
    3
    ..
    
    
    CSV Order:
    |   Player  |   Round   |   Opponent    |   points  |   isCaptain   |   opponent_NextWeek   |   points_NextWeek |
'''

def writeNewCSV(table):
    table = formatDictionary(table)

    with open("predictor.csv", 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(table)


#|   Player  |   Round   |   Opponent    |   points  |   isCaptain   |   opponent_NextWeek   |   points_NextWeek |
def formatDictionary(table):

    orderedList = [['Player', 'Round', 'Opponent', 'Points', 'isCaptain', 'Opponent_NextWeek', 'Points_NextWeek']]
    for playerList in table:
        #player = table[player]
        for player in playerList:
            maxGameweeks = len(playerList[player])
            for i in range (1, maxGameweeks):
                try:
                    print(str(i) + " --> " + player)
                    current = playerList[player][str(i)]
                    newList = [player, str(i), current['opponent_team'], current['total_points'], current['isCaptain'],
                               current['opponent_NextWeek'], current['points_NextWeek']]
                    orderedList.append(newList)
                except KeyError as e:
                    print('Skipping '+str(i) +' - '+player+'. Reason:"%s"' % str(e))
    return orderedList
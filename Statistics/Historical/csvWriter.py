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
        writer.writerow(table[0])

        maximum = 1
        for i in range (1, 39):
            for j in range(1, len(table)):
                if(int(table[j][1]) == i):
                    maximum = i
                    writer.writerow(table[j])


def formatDictionary(table):

    orderedList = [['Player', 'Round',
                    'Opponent', 'Opponent_FDR', 'isHome', 'Points',
                    'Opponent_PrevWeek', 'Opponent_FDR_PrevWeek', 'isHome_PrevWeek', 'Points_PrevWeek',
                    'Opponent_2PrevWeek', 'Opponent_FDR_2PrevWeek', 'isHome_2PrevWeek', 'Points_2PrevWeek',
                    'isCaptain']]

    for playerList in table:
        for player in playerList:
            maxGameweeks = 0
            for gw in playerList[player]:
                if(int(gw) > maxGameweeks):
                    maxGameweeks = int(gw)

            for i in range (1, maxGameweeks+1):
                try:
                    print(str(i) + " --> " + player)
                    current = playerList[player][str(i)]
                    newList = [player, str(i), current['opponent_team'], current['opponent_FDR'], current['was_home'], current['total_points'],
                               current['opponent_PrevWeek'], current['opponent_FDR_PrevWeek'], current['was_home_PrevWeek'], current['points_PrevWeek'],
                               current['opponent_2PrevWeek'], current['opponent_FDR_2PrevWeek'], current['was_home_2PrevWeek'], current['points_2PrevWeek'],
                               current['isCaptain']]
                    orderedList.append(newList)
                except KeyError as e:
                    print('Skipping '+str(i) +' - '+player+'. Reason:"%s"' % str(e))
    return orderedList
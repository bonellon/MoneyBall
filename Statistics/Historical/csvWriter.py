import csv
import Statistics.Historical.Teams as Teams
import json
import requests
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
def getFPL():
    url = "https://fantasy.premierleague.com/drf/bootstrap-static"
    r = requests.get(url)
    return json.loads(r.text)


def getTeam(FPL, currentOpponent):
    for team in FPL["teams"]:
        current = int(team["current_event_fixture"][0]["opponent"])
        print(currentOpponent)
        if(int(current) == int(currentOpponent)):
            opponent = int(team['next_event_fixture'][0]['opponent'])
            isHome = int(team['next_event_fixture'][0]['is_home'])
            return opponent, isHome


def writeNewCSV(table):
    table = formatDictionary(table)
    FPL = getFPL()

    with open("predictor.csv", 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(table[0])

        maximum = 1
        for i in range (1, 39):
            for j in range(1, len(table)):
                if(int(table[j][1]) == i):
                    maximum = i
                    writer.writerow(table[j])

    with open("predictor.csv", 'r') as csvFile:
        reader = csv.reader(csvFile)
        gwList = list(reader)
        latestGW = []
        for i in range(1, len(gwList)):
            if(int(gwList[i][1]) == maximum and int(gwList[i][6]) > 0):
                latestGW.append(gwList[i])

    newGW = []
    for player in latestGW:

        #player
        current = [player[0], str(int(player[1])+1)]

        #opponent
        team, isHome = getTeam(FPL, player[2])
        current.append(team)
        current.append(Teams.GetFDR(team, isHome))
        current.append(isHome)

        #points, minutes
        current.append(0)
        current.append(90)

        #Previous week
        current.append(player[2])
        current.append(player[3])
        current.append(player[4])
        current.append(player[5])

        #2 Weeks ago
        current.append(player[7])
        current.append(player[8])
        current.append(player[9])
        current.append(player[10])

        #isCaptain = 0
        current.append(0)

        newGW.append(current)

    with open("Predictor.csv", 'a+', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(newGW)


def formatDictionary(table):

    orderedList = [['Player', 'Round',
                    'Opponent', 'Opponent_FDR', 'isHome', 'Points', 'minutes',
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
                    newList = [player, str(i), current['opponent_team'], current['opponent_FDR'], current['was_home'], current['total_points'], current['minutes'],
                               current['opponent_PrevWeek'], current['opponent_FDR_PrevWeek'], current['was_home_PrevWeek'], current['points_PrevWeek'],
                               current['opponent_2PrevWeek'], current['opponent_FDR_2PrevWeek'], current['was_home_2PrevWeek'], current['points_2PrevWeek'],
                               current['isCaptain']]
                    orderedList.append(newList)
                except KeyError as e:
                    print('Skipping '+str(i) +' - '+player+'. Reason:"%s"' % str(e))
    return orderedList
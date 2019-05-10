import csv
import Statistics.Historical.Teams as Teams
import Statistics.Historical.TeamsEnum as TeamsEnum
import json
import requests

import Statistics.BettingData as bettingData
import Statistics.BettingPredictor as bettingPredictor
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
        if(int(current) == int(currentOpponent)):
            opponent = int(team['next_event_fixture'][0]['opponent'])
            isHome = int(team['next_event_fixture'][0]['is_home'])
            return opponent, isHome


#Get ict_index, threat, creativity, influence, trasnfers_balance,
def getPlayerStats(FPL, player):
    player = player.lower()
    for elem in FPL['elements']:
        if(player == elem['web_name'].lower() or player == elem['first_name'].lower() or player == elem['second_name'].lower()):
            ict = float(elem['ict_index'])/20
            threat = float(elem['threat'])/10
            creativity = float(elem['creativity'])/10
            influence = float(elem['influence'])/10
            transferBalance = int(elem['transfers_in_event']) - int(elem['transfers_out_event'])
            elementID = int(elem['id'])
            return ict, threat, creativity, influence, transferBalance, elementID

    print("getPlayerStats: Skipping %s -> Web_Name not found", player)
    return 0,0,0,0,0


def writeNewCSV(table):
    table = formatDictionary(table)[0]
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

        #ICT_index, Threat, Creativity, Influence, Transfers_Balance
        playerData = getPlayerStats(FPL, player[0])
        current.append(playerData[0])
        current.append(playerData[1])
        #current.append(playerData[2])
        current.append(playerData[3])
        current.append(playerData[4])

        #value, bps
        current.append(player[20])
        current.append(player[21])

        #defenseOdds, attackOdds
        gwOdds = table[1]

        if(str((int(player[1])+1)) in gwOdds):
            gwDef = gwOdds[int(player[1]) + 1]['Defense']
            gwAtt = gwOdds[int(player[1]) + 1]['Offence']

            for i in range(0, len(gwDef) - 1):
                if gwAtt[i][0] == int(current['opponent_team']):
                    current.append(gwAtt[i][1])

                if gwDef[i][0] == int(current['opponent_team']):
                    current.append(gwDef[i][1])

        newGW.append(current)

    with open("Predictor.csv", 'a+', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(newGW)


def getGWOdds():

    import os

    filepath = '../CachedJson/allOdds.txt'
    if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
        file = open(filepath , 'r')
        gwDict = json.load(file)

        return gwDict

    gwDict = {}
    for i in range(1, 38):
        gw = bettingData.getOddsGW(i)
        defenseOffence = bettingPredictor.getDefenseOffence()
        print("Round: "+str(i))
        for list in defenseOffence:
            for elem in list:
                if elem[0] == 'Leicester':
                    elem[0] = 'Leicester_City'
                elif elem[0] == 'Tottenham':
                    elem[0] = 'Spurs'
                else:
                    elem[0] = elem[0].replace(' ', '_')

            for elem in list:
                elem[0] = TeamsEnum.TeamsEnum[elem[0]].value

        gwDict.update({str(i): {
            "Defense": defenseOffence[0],
            "Offence": defenseOffence[1]
        }})

    with open('../CachedJson/allOdds.txt', 'w') as file:
        file.write(json.dumps(gwDict))
    return gwDict


    return defenseOffence


def formatDictionary(table):

    orderedList = [['Player', 'Round', 'elementID',
                    'Opponent', 'Opponent_FDR', 'isHome', 'Points', 'minutes',
                    'Opponent_PrevWeek', 'Opponent_FDR_PrevWeek', 'isHome_PrevWeek', 'Points_PrevWeek',
                    'Opponent_2PrevWeek', 'Opponent_FDR_2PrevWeek', 'isHome_2PrevWeek', 'Points_2PrevWeek',
                    'isCaptain', 'ICT_index', 'Threat','Influence', 'Transfers_Balance', 'Value', 'BPS', 'DefenseOdds', 'OffenceOdds']]

    gwOdds = getGWOdds()

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
                    newList = [player, str(i), current['elementID'], current['opponent_team'], current['opponent_FDR'], current['was_home'], current['total_points'], current['minutes'],
                               current['opponent_PrevWeek'], current['opponent_FDR_PrevWeek'], current['was_home_PrevWeek'], current['points_PrevWeek'],
                               current['opponent_2PrevWeek'], current['opponent_FDR_2PrevWeek'], current['was_home_2PrevWeek'], current['points_2PrevWeek'],
                               current['isCaptain'], current['ict_index'], current['threat'], current['influence'], current['transfers_balance'],
                               current['value'], current['bps']]

                    if str(i) in gwOdds:
                        gwDef = gwOdds[str(i)]['Defense']
                        gwAtt = gwOdds[str(i)]['Offence']

                        for i in range (0, len(gwDef)):
                            if gwAtt[i][0] == int(current['opponent_team']):
                                newList.append(gwAtt[i][1])

                            if gwDef[i][0] == int(current['opponent_team']):
                                newList.append(gwDef[i][1])



                    orderedList.append(newList)
                except KeyError as e:
                    print('Skipping '+str(i) +' - '+player+'. Reason:"%s"' % str(e))
    return orderedList, gwOdds
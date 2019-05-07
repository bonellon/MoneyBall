import os
import csv
from pathlib import Path

import Statistics.Historical.csvWriter as csvWriter
import Statistics.Historical.Teams as Teams

CAPTAIN_POINTS = 20
BASEPATH = str(Path(__file__).parents[2]) + "\\External\\vaastav\\data\\2018-19\\players"

keep = ['round', 'opponent_team', 'opponent_FDR', 'was_home', 'total_points', 'minutes', 'points_PrevWeek',
        'was_home_PrevWeek',
        'opponent_PrevWeek', 'opponent_FDR_PrevWeek', 'points_2PrevWeek', 'was_home_2PrevWeek', 'opponent_2PrevWeek',
        'opponent_FDR_2PrevWeek', 'minutes_PrevWeek', 'ict_index', 'threat', 'creativity', 'influence',
        'transfers_balance', 'value', 'bps']

currentPlayer = ""


def updateCurrentPlayer(playerFolder):
    global currentPlayer
    currentPlayer = playerFolder.split('\\')
    currentPlayer = currentPlayer[len(currentPlayer) - 1].split('_')[1]


def getPlayerGameweekCSV(playerFolder):
    updateCurrentPlayer(playerFolder)
    playerFile = playerFolder + "\\gw.csv"

    playerDict = addTotalPointsPrevWeeks(playerFile)
    if (playerDict == {}):
        return None
    playerTable = getPlayerStatistics(playerDict)
    playerTable = addIsCaptain(playerTable)
    return addOpponentFDR(playerTable)


def addTotalPointsPrevWeeks(file):
    newCSV = dict()
    lineCounter = 0
    with open(file, 'r') as csvFile:
        for line in csvFile:
            line = line.strip().split(",")
            newCSV[lineCounter] = line
            lineCounter += 1
    if (lineCounter == 0):
        return newCSV

    if ("points_PrevWeek" in newCSV[0]):
        return newCSV

    newCSV[0].append('points_PrevWeek')
    newCSV[0].append('was_home_PrevWeek')
    newCSV[0].append('opponent_PrevWeek')
    newCSV[0].append('opponent_FDR_PrevWeek')
    newCSV[0].append('minutes_PrevWeek')

    newCSV[0].append('points_2PrevWeek')
    newCSV[0].append('was_home_2PrevWeek')
    newCSV[0].append('opponent_2PrevWeek')
    newCSV[0].append('opponent_FDR_2PrevWeek')

    '''
        ROW POSITIONS

        points      46
        was_home    51
        opponent    30
        minutes     27
    '''

    with open(file, 'w', newline='') as csvFile:
        newCSV[1].append(0)
        newCSV[1].append(0)
        newCSV[1].append(0)
        newCSV[1].append(0)
        newCSV[1].append(1)

        newCSV[1].append(0)
        newCSV[1].append(0)
        newCSV[1].append(0)
        newCSV[1].append(0)

        newCSV[2].append(newCSV[1][46])

        isHome = {True: 1, False: 0}[newCSV[1][51] == 'True']

        newCSV[2].append(isHome)
        newCSV[2].append(newCSV[1][30])
        newCSV[2].append(Teams.GetFDR(int(newCSV[1][30]), isHome))
        newCSV[2].append(newCSV[1][27])

        newCSV[2].append(0)
        newCSV[2].append(0)
        newCSV[2].append(0)
        newCSV[2].append(0)

        for i in range(3, len(newCSV)):
            row = newCSV[i]
            prevRow = newCSV[i - 1]
            prevRow2 = newCSV[i - 2]

            pointsPW = prevRow[46]
            homePW = {True: 1, False: 0}[prevRow[51] == 'True']
            opponentPW = prevRow[30]
            FDR_PW = Teams.GetFDR(int(opponentPW), int(homePW))
            minutes_PW = int(prevRow[27])

            pointsPW2 = prevRow2[46]
            homePW2 = {True: 1, False: 0}[prevRow2[51] == 'True']
            opponentPW2 = prevRow[30]
            FDR_PW2 = Teams.GetFDR(int(opponentPW2), int(homePW2))

            row.append(pointsPW)
            row.append(homePW)
            row.append(opponentPW)
            row.append(FDR_PW)
            row.append(minutes_PW)

            row.append(pointsPW2)
            row.append(homePW2)
            row.append(opponentPW2)
            row.append(FDR_PW2)

        writer = csv.writer(csvFile)
        for key, value in newCSV.items():
            writer.writerow(value)
    return newCSV


def iteratePlayers():
    allPlayer = []
    for folderName in os.listdir(BASEPATH):
        playerTable = getPlayerGameweekCSV(BASEPATH + "\\" + folderName)
        if (playerTable != None):
            allPlayer.append(playerTable)
    return allPlayer


def getPlayerStatistics(gwDict):
    filteredDict = dict()
    keepPositions = {}
    for i in range(0, len(gwDict[0])):
        if (gwDict[0][i] in keep):
            for key in keep:
                if (key == gwDict[0][i]):
                    keepPositions[key] = i

    filteredDict[currentPlayer] = dict()
    try:

        for i in range(1, len(gwDict)):
            round = gwDict[i][keepPositions['round']]
            filteredDict[currentPlayer][round] = dict()
            for key, value in keepPositions.items():
                if (key == "was_home"):
                    toAppend = 0
                    if (gwDict[i][value] == "True"):
                        toAppend = 1
                    filteredDict[currentPlayer][round][key] = toAppend
                else:
                    filteredDict[currentPlayer][round][key] = gwDict[i][int(value)]

    except:
        print("ERROR")
    return filteredDict


def addIsCaptain(playerLists):
    print(playerLists)
    for player in playerLists:
        for gw in playerLists[player]:
            if (int(playerLists[player][gw]['total_points']) >= CAPTAIN_POINTS):
                playerLists[player][gw]['isCaptain'] = 1
            else:
                playerLists[player][gw]['isCaptain'] = 0

            playerLists[player][gw]['player'] = currentPlayer
    return playerLists


def addOpponentFDR(playerLists):
    for player in playerLists:
        for gw in playerLists[player]:
            currentOpponent = int(playerLists[player][gw]['opponent_team'])
            isHome = playerLists[player][gw]['was_home']
            FDR = Teams.GetFDR(currentOpponent, isHome)

            playerLists[player][gw]['opponent_FDR'] = FDR
    return playerLists


def removeNonPlaying(playerList):
    for players in list(playerList):
        for player in list(players):
            for gameweek in list(players[player]):
                if (int(players[player][gameweek]['minutes_PrevWeek']) == 0):
                    players[player].pop(gameweek, None)

    return playerList


# ramseyPath = "C:/Users/Nicky/Documents/Moneyball/MoneyBall_Code/External/vaastav/data/2018-19/players/Aaron_Ramsey_14/gw.csv"
# START
playersList = iteratePlayers()
playersList = removeNonPlaying(playersList)
csvWriter.writeNewCSV(playersList)

# Y = 0 if player < 4 points
# Y = 1 if player >= 4 points
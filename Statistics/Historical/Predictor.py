import os
import csv
import pandas as pd

from Statistics.Historical.Teams import Teams

BASEPATH = "C:\\Users\\Nicky\\Documents\\Moneyball\\MoneyBall_Code\\External\\vaastav\\data\\2018-19\\players"

keep = ['round', 'opponent_team', 'total_points', 'opponent_NextWeek', 'points_NextWeek']

currentPlayer = ""

def updateCurrentPlayer(playerFolder):
    global currentPlayer
    currentPlayer = playerFolder.split('\\')
    currentPlayer = currentPlayer[len(currentPlayer)-1].split('_')[1]


def getPlayerGameweekCSV(playerFolder):
    updateCurrentPlayer(playerFolder)
    playerFile = playerFolder+"\\gw.csv"

    playerDict = addTotalPointsNextWeek(playerFile)
    playerTable2 = getPlayerStatistics(playerDict)
    return addIsCaptain2(playerTable2)

def addTotalPointsNextWeek(file):
    newCSV = dict()
    lineCounter = 0
    with open(file, 'r') as csvFile:
        for line in csvFile:
            line = line.strip().split(",")
            newCSV[lineCounter] = line
            lineCounter += 1

    if ("opponent_NextWeek" in newCSV[0]):
        return newCSV

    newCSV[0].append('opponent_NextWeek')
    newCSV[0].append('points_NextWeek')

    with open(file, 'w', newline='') as csvFile:

        for i in range(1,len(newCSV)-1):
            row = newCSV[i]
            nextRow = newCSV[i+1]

            opponentNW = Teams(int(nextRow[30])).name
            pointsNW = nextRow[46]

            row.append(opponentNW)
            row.append(pointsNW)

        newCSV[len(newCSV)-1].append(0)
        newCSV[len(newCSV)-1].append(0)
        writer = csv.writer(csvFile)
        for key,value in newCSV.items():
            writer.writerow(value)
    return newCSV


def iteratePlayers():
    allPlayer = []
    for folderName in os.listdir(BASEPATH):
        playerTable = getPlayerGameweekCSV(BASEPATH+"\\"+folderName)
        allPlayer.append(playerTable)
    return allPlayer

def getPlayerStatistics(gwDict):
    filteredDict = dict()
    keepPositions = {}
    for i in range(0, len(gwDict[0])):
        if(gwDict[0][i] in keep):
            for key in keep:
                if(key == gwDict[0][i]):
                    keepPositions[key] = i

    filteredDict[currentPlayer] = dict()
    for i in range(1, len(gwDict)):
        round = gwDict[i][keepPositions['round']]
        filteredDict[currentPlayer][round] = dict()
        for key,value in keepPositions.items():
            filteredDict[currentPlayer][round][key] = gwDict[i][int(value)]
    return filteredDict

def writeNewCSV(table):

    with open("predictor.csv", 'w', newline='') as csvFile:
        w = csv.writer(csvFile)
        keys = table[0][list(table[0])[0]]['1'].keys()
        w.writerow(keys)

        for player in table:
            current = list(player.keys())[0]
            for gw in player[current]:
                write = player[current][gw]
                w.writerow(write.values())



def addIsCaptain2(playerLists):
    print(playerLists)
    for player in playerLists:
        for gw in playerLists[player]:
            if (int(playerLists[player][gw]['total_points']) >= 4):
                playerLists[player][gw]['isCaptain'] = 1
            else:
                playerLists[player][gw]['isCaptain'] = 0

            playerLists[player][gw]['player'] = currentPlayer
    return playerLists

#ramseyPath = "C:/Users/Nicky/Documents/Moneyball/MoneyBall_Code/External/vaastav/data/2018-19/players/Aaron_Ramsey_14/gw.csv"
#START
playersList = iteratePlayers()

#addTotalPointsNextWeek(ramseyPath)

#table = getPlayerStatistics(ramseyPath)
writeNewCSV(playersList)



#Y = 0 if player < 4 points
#Y = 1 if player >= 4 points
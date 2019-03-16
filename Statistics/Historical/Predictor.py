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
    playerTable = getPlayerStatistics(playerFile)
    playerTable2 = getPlayerStatistics2(playerDict)
    return addIsCaptain(playerTable2)

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
        allPlayer.append(playerTable[1:])
    return allPlayer

def getPlayerStatistics2(gwDict):
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

def getPlayerStatistics(playerFile):
    with open(playerFile, 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        isFirst = True
        table = []

        keepPosition = []
        for row in csv_reader:
            rowArr = []
            if isFirst:
                for i in range(len(row)):
                    if row[i] in keep:
                        keepPosition.append(i)
                        rowArr.append(row[i])
                isFirst = False
            else:
                for position in keepPosition:
                    if (position == 30):
                        rowArr.append(Teams(int(row[position])).name)
                    else:
                        rowArr.append(row[position])
            table.append(rowArr)
    return table

def writeNewCSV(table):

    #with open("predictor.csv", 'w', newline='') as csvFile:

    for row in table:
        isFirst = True
        if(isFirst):
            isFirst = False
        print(row)

def addIsCaptain(table):
    isFirst = True
    totalPoints = 0
    for row in table:
        if(isFirst):
            position = 0
            for elem in row:
                if(elem == 'total_points'):
                    totalPoints = position
                position = position + 1

            row.append("isCaptain")
            row.append("player")

            isFirst = False

        else:
            points = int(row[totalPoints])
            if(points >= 4):
                row.append(1)
            else:
                row.append(0)
            row.append(currentPlayer)
    return table


#ramseyPath = "C:/Users/Nicky/Documents/Moneyball/MoneyBall_Code/External/vaastav/data/2018-19/players/Aaron_Ramsey_14/gw.csv"
#START
playersList = iteratePlayers()

#addTotalPointsNextWeek(ramseyPath)

#table = getPlayerStatistics(ramseyPath)
writeNewCSV(playersList)



#Y = 0 if player < 4 points
#Y = 1 if player >= 4 points
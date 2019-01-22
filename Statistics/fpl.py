# https://github.com/277roshan/MachineLearningFinalProject/blob/master/Machine%20Learning%20Final%20Project.ipynb

import csv
import json
from collections import OrderedDict

import requests

url = "https://fantasy.premierleague.com/drf/bootstrap-static"

requiredColumns = ['id', 'web_name', 'team_code', 'element_type', 'status', 'now_cost', 'chance_of_playing_next_round',
                   'value_season', 'minutes', 'goals_scored', 'assists', 'saves', 'clean_sheets', 'goals_conceded',
                   'bps', 'ict_index', 'form', 'ea_index', 'threat', 'transfers_in', 'transfers_in_event',
                   'transfers_out', 'transfers_out_event', 'total_points', 'ep_next', 'event_points']

commonColumns = ['id', 'web_name', 'team_code', 'element_type', 'status', 'now_cost', 'chance_of_playing_next_round',
                 'value_season', 'minutes', 'bps', 'ict_index', 'form', 'transfers_in_event',
                 'transfers_out_event','total_points', 'ep_next', 'event_points']

goalkeeperColumns = ['clean_sheets', 'goals_conceded']
defenderColumns = ['clean_sheets', 'goals_conceded', 'threat']
midfielderColumns = ['goals_scored', 'assists', 'clean_sheets', 'goals_conceded', 'threat']
forwardColumns = ['goals_scored', 'assists', 'threat']

def getFPLData():
    r = requests.get(url)
    data = json.loads(r.text)
    all_players = data['elements']
    return all_players

def getElementType(object):
    for element in object:
        if element == "element_type":
            return object[0]
    return 0

def CleanDataCSV(players):
    elementTypePosition = 0

    #Define empty list with size requiredColumns
    rows = [None] * len(requiredColumns)

    #Populate rows
    newPlayers = {}
    for player in players:
        newplayer = {}
        if player['element_type'] == 1:
            newplayer = getPlayerData(player, goalkeeperColumns)
        elif player['element_type'] == 2:
            newplayer = getPlayerData(player, defenderColumns)
        elif player['element_type'] == 3:
            newplayer = getPlayerData(player, midfielderColumns)
        elif player['element_type'] == 4:
            newplayer = getPlayerData(player, forwardColumns)

        newPlayers[newplayer["id"]] = newplayer

    print(len(newPlayers))
    newPlayers = checkPlayerStatus(newPlayers)
    print(len(newPlayers))
    '''
    isFirst = True
    
    for row in readCSV:
        rowContents = []
        for i in rows:
            rowContents.append(row[i])
        if isFirst:
            writeToCSV("stats/goalkeepers.csv", rowContents, "w")
            writeToCSV("stats/defenders.csv", rowContents, "w")
            writeToCSV("stats/midfielders.csv", rowContents, "w")
            writeToCSV("stats/forwards.csv", rowContents, "w")
            isFirst = False
        else:
            filename = "undefined.csv"
            elementType = int(row[elementTypePosition])

            if elementType == 1:
                filename = "stats/goalkeepers.csv"
            elif elementType == 2:
                filename = "stats/defenders.csv"
            elif elementType == 3:
                filename = "stats/midfielders.csv"
            elif elementType == 4:
                filename = "stats/forwards.csv"
            writeToCSV(filename, rowContents, "a")
    '''

#Iterate through players dict and return all that have chance of playing next round higher than 75%
def checkPlayerStatus(players):

    newDict = {}
    for key, value in players.items():
        if (value['chance_of_playing_next_round'] is not None) and (int(value['chance_of_playing_next_round']) > 75):
            newDict[key] = value

    return newDict


def getPlayerData(player, columns):
    list = commonColumns + columns
    newlist = []
    for item in list:
        newlist.append([item, ''])

    newPlayer = OrderedDict(newlist)

    for key in newPlayer:
            newPlayer[key] = player[key]

    return newPlayer


def writeToCSV(filename, object, writeOrAppend):
    with open(filename, writeOrAppend, newline='') as fp:
        wr = csv.writer(fp, dialect="excel")
        wr.writerow(object)

players = getFPLData()
CleanDataCSV(players)

'''
1. Remove injured players <50% chance of playing
'''

'''
2. Remove extra columns from CSVs
'''
'''
3. 
'''
'''
'''
'''
'''
'''
'''

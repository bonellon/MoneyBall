# https://github.com/277roshan/MachineLearningFinalProject/blob/master/Machine%20Learning%20Final%20Project.ipynb

import csv
import json
from collections import OrderedDict
import Statistics.PredictGoalkeeper as predictGoalkeeper
import Statistics.PredictDefender as predictDefender
import Statistics.PredictMidfielder as predictMidfielder
import Statistics.PredictForward as predictForward

import requests

url = "https://fantasy.premierleague.com/drf/bootstrap-static"

requiredColumns = ['id', 'web_name', 'team_code', 'element_type', 'status', 'now_cost', 'chance_of_playing_next_round',
                   'value_season', 'minutes', 'goals_scored', 'assists', 'saves', 'clean_sheets', 'goals_conceded',
                   'bps', 'ict_index', 'form', 'ea_index', 'threat', 'transfers_in', 'transfers_in_event',
                   'transfers_out', 'transfers_out_event', 'total_points', 'ep_next', 'event_points']

commonColumns = ['id', 'web_name', 'team_code', 'element_type', 'status', 'now_cost', 'chance_of_playing_next_round',
                 'value_season', 'minutes', 'bps', 'ict_index', 'form', 'transfers_in_event',
                 'transfers_out_event', 'total_points', 'ep_next', 'event_points']

goalkeeperColumns = ['clean_sheets', 'goals_conceded']
defenderColumns = ['clean_sheets', 'goals_conceded', 'threat']
midfielderColumns = ['goals_scored', 'assists', 'clean_sheets', 'goals_conceded', 'threat']
forwardColumns = ['goals_scored', 'assists', 'threat']

gameweek = 0

def getFPLData():
    r = requests.get(url)
    return json.loads(r.text)

def getElementType(object):
    for element in object:
        if element == "element_type":
            return object[0]
    return 0

def getPlayersData():
    data = getFPLData()
    all_players = data['elements']
    getCurrentGameweek(data['events'])
    print("Gameweek: ",gameweek)
    return all_players

def getCurrentGameweek(events):
    for event in events:
        if event['is_current']:
            global gameweek
            gameweek = event['id']
            continue

def getTeamIds():

    teams = {}
    data = getFPLData()
    teamsData = data['teams']
    for team in teamsData:
        teams[team['short_name']] = {"id": team['id'], "name": team["name"]}
    return teams

def CleanDataCSV(players):
    elementTypePosition = 0

    # Define empty list with size requiredColumns
    rows = [None] * len(requiredColumns)

    # Populate rows
    newPlayers = {}
    goalkeepers = []
    defenders = []
    midfielders = []
    forwards = []
    for player in players:
        newplayer = {}
        if player['element_type'] == 1:
            newplayer = getPlayerData(player, goalkeeperColumns)
            if checkPlayerStatus(newplayer):
                goalkeepers.append(newplayer.values())
        elif player['element_type'] == 2:
            newplayer = getPlayerData(player, defenderColumns)
            if checkPlayerStatus(newplayer):
                defenders.append(newplayer.values())
        elif player['element_type'] == 3:
            newplayer = getPlayerData(player, midfielderColumns)
            if checkPlayerStatus(newplayer):
                midfielders.append(newplayer.values())
        elif player['element_type'] == 4:
            newplayer = getPlayerData(player, forwardColumns)
            if checkPlayerStatus(newplayer):
                forwards.append(newplayer.values())

        newPlayers[newplayer["id"]] = newplayer

    print(len(newPlayers))
    newPlayers = checkPlayersStatus(newPlayers)
    print(len(newPlayers))
    print(len(goalkeepers), " ", len(defenders), " ", len(midfielders), " ", len(forwards), " ",
          (len(goalkeepers) + len(defenders) + len(midfielders) + len(forwards)))

    writeManyToCSV("stats/goalkeepers.csv", goalkeepers, commonColumns + goalkeeperColumns)
    writeManyToCSV("stats/defenders.csv", defenders, commonColumns + defenderColumns)
    writeManyToCSV("stats/midfielders.csv", midfielders, commonColumns + midfielderColumns)
    writeManyToCSV("stats/forwards.csv", forwards, commonColumns + forwardColumns)


# Iterate through players dict and return all that have chance of playing next round higher than 75%
def checkPlayersStatus(players):
    newDict = {}
    for key, value in players.items():
        if (value['chance_of_playing_next_round'] is not None) and (int(value['chance_of_playing_next_round']) >= 75):
            newDict[key] = value
        elif (value['status'] is not None) and value['status'] == 'a':
            newDict[key] = value

    return newDict


def checkPlayerStatus(value):
    if (value['chance_of_playing_next_round'] is not None) and (int(value['chance_of_playing_next_round']) >= 75):
        return True
    elif (value['status'] is not None) and value['status'] == 'a':
        return True
    return False


def getPlayerData(player, columns):
    list = commonColumns + columns
    newlist = []
    for item in list:
        newlist.append([item, ''])

    newPlayer = OrderedDict(newlist)

    for key in newPlayer:
        newPlayer[key] = player[key]

    return newPlayer


def writeManyToCSV(filename, object, headers):
    with open(filename, 'w', newline='') as fp:
        wr = csv.writer(fp, dialect="excel")
        wr.writerow(headers)
        for row in object:
            wr.writerow(row)


def writeToCSV(filename, object, writeOrAppend):
    with open(filename, writeOrAppend, newline='') as fp:
        wr = csv.writer(fp, dialect="excel")
        wr.writerow(object)

'''
1. Remove injured players <50% chance of playing
'''

'''
2. Remove extra columns from CSVs
'''
'''
3. Goalkeeper predictions
    >>EP_Next, Cleansheets, Goals Conceeded (?), TransfersIn_Event, Now_Cost, Form
'''

'''
4. Given list of topX players [Goalkeepers, Defenders etc.] 
    format into a human readable form. 
    Display ID, PlayerName, EP_Next
'''
def formatResults(players):
    result = {}
    for player in players:
        player = player[1]
        result[player['id']] = {'name': player['web_name'], 'id': player['id'], 'ep_next': player['ep_next'],
                                'predictedValue': player['predictedValue'], 'transferRatio':player['transferRatio']}
    return result
'''
5. Get fixture difficulty rating. 
Must consider opponent form & Home/Away match 
'''

'''
'''

#players = getPlayersData()
#CleanDataCSV(players)


topGoalkeepers = formatResults(predictGoalkeeper.PredictGoalkeepers())
for x in topGoalkeepers:
    print(topGoalkeepers[x])

print()
topDefenders = formatResults(predictDefender.PredictDefenders())
for x in topDefenders:
    print(topDefenders[x])

print()
topMidfielders = formatResults(predictMidfielder.PredictMidfielders())
for x in topMidfielders:
    print(topMidfielders[x])

print()
topForwards = formatResults(predictForward.PredictForwards())
for x in topForwards:
    print(topForwards[x])


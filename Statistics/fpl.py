# https://github.com/277roshan/MachineLearningFinalProject/blob/master/Machine%20Learning%20Final%20Project.ipynb

import csv
import json
import requests

url = "https://fantasy.premierleague.com/drf/bootstrap-static"

requiredColumns = ['id', 'web_name', 'team_code', 'element_type', 'status', 'now_cost', 'chance_of_playing_next_round',
                   'value_season', 'minutes', 'goals_scored', 'assists', 'saves', 'clean_sheets', 'goals_conceded',
                   'bps', 'ict_index', 'form', 'ea_index', 'threat', 'transfers_in', 'transfers_in_event',
                   'transfers_out', 'transfers_out_event', 'total_points', 'ep_next', 'event_points']

def getElementType(object):
    for element in object:
        if element == "element_type":
            return object[0]
    return 0

def CleanDataCSV():
    elementTypePosition = 0
    with open(csvfile, "r", newline='') as fp:
        reader = csv.reader(fp)
        readCSV = list(reader)

        #Define empty list with size requiredColumns
        rows = [None] * len(requiredColumns)

        #Populate rows
        for i in range(len(readCSV[0])):
            if readCSV[0][i] in requiredColumns:
                rows[requiredColumns.index(readCSV[0][i])] = i

                if readCSV[0][i] == "element_type":
                    elementTypePosition = i

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


def writeToCSV(filename, object, writeOrAppend):
    with open(filename, writeOrAppend, newline='') as fp:
        wr = csv.writer(fp, dialect="excel")
        wr.writerow(object)


def getFPLData():
    r = requests.get(url)
    data = json.loads(r.text)
    all_players = data['elements']

    player_dict = {}
    for i in all_players:
        player_dict[i['id']] = i['web_name']

    # print(player_dict)

    scorers = []
    possible_scorers = {}
    count = 0
    n = 1

    csvfile = "data.csv"
    with open(csvfile, "w", newline='') as fp:
        wr = csv.writer(fp, dialect="excel")
        print(all_players[0])
        wr.writerow(all_players[0])
        for dict in all_players:
            rowList = []
            for k,v in dict.items():
                print(v)
                rowList.append(v)
            wr.writerow(rowList)

getFPLData()
CleanDataCSV()

'''
1. Remove injured players <50% chance of playing
'''

'''
2. Remove extra columns from CSVs
'''
requiredColumns = ['goals_scored', 'assists', 'saves', 'clean_sheets', 'goals_conceded',
                   'ea_index', 'transfers_in', 'transfers_out']


commonColumns = ['id', 'web_name', 'team_code', 'element_type', 'status', 'now_cost', 'chance_of_playing_next_round',
                 'value_season', 'minutes', 'bps', 'ict_index', 'form', 'threat', 'transfers_in_event',
                 'transfers_out_event','total_points', 'ep_next', 'event_points']
goalkeeperColumns = ['clean_sheets', 'goals_conceded']
defenderColumns = ['clean_sheets', 'goals_conceded']
midfielderColumns = ['goals_scored', 'assists', 'clean_sheets', 'goals_conceded']
forwardColumns = ['goals_scored', 'assists']

'''
3. 
'''
'''
'''
'''
'''
'''
'''

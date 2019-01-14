# https://github.com/277roshan/MachineLearningFinalProject/blob/master/Machine%20Learning%20Final%20Project.ipynb

import csv
import json
import requests

requiredColumns = ['id',
                   'web_name',
                   'team_code',
                   'element_type',
                   'status',
                   'now_cost',
                   'chance_of_playing_next_round',
                   'value_season',
                   'minutes',
                   'goals_scored',
                   'assists',
                   'saves',
                   'clean_sheets',
                   'goals_conceded',
                   'bps',
                   'ict_index',
                   'form',
                   'ea_index',
                   'threat',
                   'transfers_in',
                   'transfers_in_event',
                   'transfers_out',
                   'transfers_out_event',
                   'total_points',
                   'ep_next']

def getElementType(object):
    for element in object:
        if element == "element_type":
            return object[0]
    return 0

def CleanDataCSV():
    contents = []
    elementTypePosition = 0
    with open(csvfile, "r", newline='') as fp:
        reader = csv.reader(fp)
        readCSV = list(reader)
        rows = []
        for i in range(len(readCSV[0])):
            if readCSV[0][i] in requiredColumns:
                rows.append(i)
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


url = "https://fantasy.premierleague.com/drf/bootstrap-static"
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

CleanDataCSV()
'''
try:
    for i in player_dict:
        print(i, player_dict[i])

        url = "https://fantasy.premierleague.com/drf/element-summary/" + str(i)
        r = requests.get(url)
        data = json.loads(r.text)
        # data['fixtures']
        value = data['history']

        # print value
        all_features = []
        labels = []
        a = False;
        for j in value:
            #         print i['total_points'],i['kickoff_time_formatted']
            features = [int(j['goals_scored']), int(j['total_points']), int(j['clean_sheets'])]
            all_features.append(features)
            if a:
                if j['total_points'] >= 8:
                    labels.append(1)
                else:
                    labels.append(0)
            a = True

        first_test = all_features.pop()
        first_test = all_features.pop()
        first_test = all_features.pop()
        first_test = all_features.pop()
        actual_point = all_features.pop()
        first_test = all_features#.pop()

        label_test = labels.pop()
        label_test = labels.pop()
        label_test = labels.pop()
        label_test = labels.pop()
        label_test = labels#.pop()

        #print(len(all_features))
        #print(len(labels))
        print(first_test)

        features_train = all_features
        labels_train = labels

        try:
            clf = GaussianNB()
            t0 = time()
            clf.fit(features_train, labels_train)

            print("training time:", round(time() - t0, 3), "s")
            res = clf.predict(first_test)

            if res[0] == 1:
                possible_scorers[player_dict[i]] = actual_point[1]

            if res[0] == label_test:
                count += 1
                if res[0] == 1:
                    scorers.append(player_dict[i])

            if n == 651:
                break
            n += 1
        except ValueError as e:
            print("ValueError: ", e)
            pass
except Exception as e:
    print("Error: ", e)
    pass
print(scorers)
#print(possible_scorers)

sorted = sorted(possible_scorers.items(), key=lambda kv: kv[1])
print(sorted)

plot_scorers = scorers
plot_possible_scorers = possible_scorers

print(count / 651.0 * 100)

b = 0
for i in plot_possible_scorers:
    if i in plot_scorers:
        print(i)
    b += 1
'''

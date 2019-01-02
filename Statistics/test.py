# https://github.com/277roshan/MachineLearningFinalProject/blob/master/Machine%20Learning%20Final%20Project.ipynb

import csv
import json

import requests

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
with open(csvfile, "w") as fp:
    wr = csv.writer(fp, dialect="excel")
    print(all_players[0])
    wr.writerow(all_players[0])
    for dict in all_players:
        rowList = []
        for k,v in dict.items():
            print(v)
            rowList.append(v)
        wr.writerow(rowList)
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

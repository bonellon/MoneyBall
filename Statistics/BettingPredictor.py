import csv


# Goalkeepers + Defenders
# Result and Both teams to score 1/n N/n
def calculateBestDefense():

    teamProbabilities = []
    with open('odds/Result&The2TeamsScore.csv', 'r') as file:

        csv_reader = csv.reader(file, delimiter=',')
        isFirst = True
        keep = ['Team1', 'Team2', '%1 & No', '%2 & No', '%N & No']
        keepPosition = []
        for row in csv_reader:
            if isFirst:
                for i in range(len(row) - 1):
                    if row[i] in keep:
                        keepPosition.append(i)
            else:
                fixture = []
                for position in keepPosition:
                    fixture.append(row[position])

                team1Cleansheet = [fixture[0], round(float(fixture[2]) + float(fixture[4]), 2)]
                team2Cleansheet = [fixture[1], round(float(fixture[3]) + float(fixture[4]), 2)]
                teamProbabilities.append(team1Cleansheet)
                teamProbabilities.append(team2Cleansheet)
            isFirst = False

    sortedProbabilities = sorted(teamProbabilities, key=lambda x: x[1])
    return sortedProbabilities
# Midfielders


# Striker
# Result and both teams to score 1/y n/y


calculateBestDefense()

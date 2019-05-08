import csv

# Goalkeepers + Defenders
# Result and Both teams to score 1/n N/n
def calculateBestDefense(keep):

    teamProbabilities = []

    import os

    current = os.path.abspath(os.curdir).split('\\')
    if current[len(current) - 1] == 'Historical':
        file = open('../odds/Result&The2TeamsScore.csv', 'r')

    else:
        file = open('odds/Result&The2TeamsScore.csv', 'r')


    csv_reader = csv.reader(file, delimiter=',')
    isFirst = True
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
    file.close()
    return sortedProbabilities


# Midfielders & Strikers
def calculateBestOffence(keep):
    teamProbabilities = []

    import os

    current = os.path.abspath(os.curdir).split('\\')
    if current[len(current) - 1] == 'Historical':
        file = open('../odds/Result&The2TeamsScore.csv', 'r')

    else:
        file = open('odds/Result&The2TeamsScore.csv', 'r')

    csv_reader = csv.reader(file, delimiter=',')
    isFirst = True

    keepPosition = []
    for row in csv_reader:
        if isFirst:
            for i in range(len(row)):
                if row[i] in keep:
                    keepPosition.append(i)
        else:
            fixture = []
            for position in keepPosition:
                fixture.append(row[position])

            team1 = [fixture[0], round(float(fixture[2]) + float(fixture[3]) + float(fixture[6]), 2)]
            team2 = [fixture[1], round(float(fixture[4]) + float(fixture[5]) + float(fixture[6]), 2)]
            teamProbabilities.append(team1)
            teamProbabilities.append(team2)
        isFirst = False

    sortedProbabilities = sorted(teamProbabilities, key=lambda x: x[1])
    file.close()
    return sortedProbabilities

# Result and both teams to score 1/y n/y

keepDefense = ['Team1', 'Team2', '%1 & No', '%2 & No', '%N & No']
keepOffence = ['Team1', 'Team2', '%1 & No','%1 & Yes', '%2 & No', '%2 & Yes', '%N & Yes']


def getDefenseOffence():

    defense = calculateBestDefense(keepDefense)
    offence = calculateBestOffence(keepOffence)
    print("Defense: ", str(defense))
    print("Offence: ", str(offence))
    return defense, offence


getDefenseOffence()
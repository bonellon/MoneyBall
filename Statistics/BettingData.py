import json
import requests

isTest = False
currentGameweek = 21
mashapeKey = "trr4b4xsHumshQ6nTWYhZnzZEdUnp1VvuQEjsnes6a8aaI5vgr"


def writeResponseToFile(fileName, text):
    file = open(fileName, 'w')
    file.write(text)
    file.close


def getEPLleagueID():
    fileName = 'getLeagues.txt'
    if isTest:
        with open(fileName, 'r') as file:
            responseText = file.read()

    else:
        response = requests.get("https://api-football-v1.p.mashape.com/leagues",
                                headers={
                                    "X-Mashape-Key": mashapeKey,
                                    "Accept": "application/json"
                                }
                                )
        responseText = response.text
        writeResponseToFile(fileName, responseText)

    data = json.loads(responseText)
    leagues = data['api']['leagues']
    league_id = 0

    for i in leagues:
        league_name = leagues[i]['name']
        league_country = leagues[i]['country']
        league_season = leagues[i]['season']
        if league_name == "Premier League" and league_country == "England" and league_season == "2018":
            league_id = i
            break

    return league_id


# get list of teams in league
def getTeams(leagueID):
    fileName = 'getTeams.txt'
    if isTest:
        with open(fileName, 'r') as file:
            responseText = file.read()

    else:
        response = requests.get("https://api-football-v1.p.mashape.com/teams/league/" + leagueID,
                                headers={
                                    "X-Mashape-Key": mashapeKey,
                                    "Accept": "application/json"
                                }
                                )
        responseText = response.text
        writeResponseToFile(fileName, responseText)

    data = json.loads(responseText)
    return data['api']['teams']


# get list of next gameweek fixtures
def getFixtures(leagueID):
    fileName = "getFixtures.txt"
    if isTest:
        with open(fileName, 'r') as file:
            responseText = file.read()

    else:
        response = requests.get("https://api-football-v1.p.mashape.com/fixtures/league/"+ leagueID,
                               headers={
                                   "X-Mashape-Key": "trr4b4xsHumshQ6nTWYhZnzZEdUnp1VvuQEjsnes6a8aaI5vgr",
                                   "Accept": "application/json"
                               }
                               )
        responseText = response.text

    data = json.loads(responseText)["api"]["fixtures"]
    writeResponseToFile(fileName, responseText)
    cleanFixtureFile(data)


def cleanFixtureFile(data):
    cleanedFixtures = []
    for fixture in data:
        current = data[fixture]['round']
        if current == ("Premier League - " + str(currentGameweek)):
            cleanedFixtures.append(data[fixture])

    file = open("getCleanedFixtures.txt", 'w')
    for fixture in cleanedFixtures:
        file.write(str(fixture))
        file.write(",")
    file.close
    return cleanedFixtures

def getOdds(fixtureID):
    fileName = "getOdds.txt"
    if isTest:
        with open(fileName, 'r') as file:
            responseText = file.read()

    else:
        response = requests.get("https://api-football-v1.p.mashape.com/odds/"+str(fixtureID),
                               headers={
                                   "X-Mashape-Key": "trr4b4xsHumshQ6nTWYhZnzZEdUnp1VvuQEjsnes6a8aaI5vgr",
                                   "Accept": "application/json"
                               }
                               )
        responseText = response.text

    data = json.loads(responseText)["api"]["odds"]
    writeResponseToFile(fileName, responseText)

# leagueID = getEPLleagueID()
#getFixtures("2")
getOdds(271)
teams = []#getTeams("2")
teamIDs = []
for team in teams:
    teamIDs.append(teams[team]['team_id'])
print(teamIDs)


# for each game in next gameweek; get odds

# store odds per fixture in csv

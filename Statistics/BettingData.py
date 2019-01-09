import json
import csv
import requests
from decimal import Decimal

isTest = True
currentGameweek = 21
requiredOdds = {"Win the match", "Both teams score", "Result & The 2 teams score", "Scorer"}
mashapeKey = "trr4b4xsHumshQ6nTWYhZnzZEdUnp1VvuQEjsnes6a8aaI5vgr"


def writeResponseToFile(fileName, text):
    file = open(fileName, 'w')
    file.write(text)
    file.close


def writeOddsToCSV(data):
    isFirst = True
    fixturesList = getFixtureNames()
    for fixtureId in data:
        teams = getFixture(fixturesList, fixtureId)
        for market in data[fixtureId]:
            marketTitle = market.title().replace(" ", "")
            fileName = "odds/" + marketTitle + ".csv"
            if (isFirst):
                f = open(fileName, 'w', newline='')
            else:
                f = open(fileName, 'a', newline='')

            w = csv.writer(f)
            if marketTitle == "WinTheMatch":
                WinTheMatchCSV(w, fixtureId, teams, data[fixtureId][market], isFirst)
            elif marketTitle == "BothTeamsScore":
                BothTeamsScoreCSV(w, fixtureId, teams, data[fixtureId][market], isFirst)
            elif marketTitle == "Result&The2TeamsScore":
                ResultAndThe2TeamsScoreCSV(w, fixtureId, teams, data[fixtureId][market], isFirst)
            f.close()
        isFirst = False


def calculateImpliedProbability(odd):
    return round((1 / Decimal(odd)) * 100, 2)


def BothTeamsScoreCSV(w, fixtureId, teams, data, isFirst):
    if isFirst:
        header = ['FixtureID', 'Team1', 'Team2', 'Yes', '%Yes', 'No', '%No']
        w.writerow(header)
    content = [fixtureId, teams[0], teams[1], data['Yes']['odd'], calculateImpliedProbability((data['Yes']['odd'])), data['No']['odd'], calculateImpliedProbability((data['No']['odd']))]
    w.writerow(content)


def ResultAndThe2TeamsScoreCSV(w, fixtureId, teams, data, isFirst):
    if isFirst:
        header = ['FixtureID', 'Team1', 'Team2', '1 & No', '1 & Yes', '2 & No', '2 & Yes', 'N & No', 'N & Yes']
        w.writerow(header)
    content = [fixtureId, teams[0], teams[1], data['1 / No']['odd'], data['1 / Yes']['odd'], data['2 / No']['odd'], data['2 / Yes']['odd'],
               data['N / No']['odd'], data['N / Yes']['odd']]
    w.writerow(content)


def WinTheMatchCSV(w, fixtureId, teams, data, isFirst):
    if isFirst:
        header = ['FixtureID', 'Team1', 'Team2', '1', 'N', '2']
        w.writerow(header)
    content = [fixtureId, teams[0], teams[1], data['1']['odd'], data['N']['odd'], data['2']['odd']]
    w.writerow(content)


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
        response = requests.get("https://api-football-v1.p.mashape.com/fixtures/league/" + leagueID,
                                headers={
                                    "X-Mashape-Key": mashapeKey,
                                    "Accept": "application/json"
                                }
                                )
        responseText = response.text

    data = json.loads(responseText)["api"]["fixtures"]
    writeResponseToFile(fileName, responseText)
    return cleanFixtureFile(data)


def cleanFixtureFile(data):
    cleanedFixtures = "{"
    for fixture in data:
        current = data[fixture]['round']
        if current == ("Premier League - " + str(currentGameweek)):
            cleanedFixtures = cleanedFixtures + "\"" + fixture + "\":" + str(data[fixture]) + ","

    cleanedFixtures = cleanedFixtures[:-1] + "}"
    cleanedFixtures = cleanedFixtures.replace("'penalty': None,", "")

    file = open("getCleanedFixtures.txt", 'w')
    file.write(cleanedFixtures)
    file.close
    return cleanedFixtures


def getFixtureNames():
    with open('getCleanedFixtures.txt', 'r') as f:
        read = f.read()
        jsonFixtures = json.loads(read.replace("'", "\"").replace('None', '"NULL"'))

        fixturesList = []
        for fixture in jsonFixtures:
            fixtureId = jsonFixtures[fixture]['fixture_id']
            homeTeam = jsonFixtures[fixture]['homeTeam']
            awayTeam = jsonFixtures[fixture]['awayTeam']

            fixture = [fixtureId, homeTeam, awayTeam]
            fixturesList.append(fixture)
    return fixturesList

def getFixture(fixturesList, fixtureId):
    for fixture in fixturesList:
        if fixture[0] == fixtureId:
            return (fixture[1], fixture[2])

def getOdds(fixtureIds):
    fileName = "getOdds.txt"
    if isTest:
        with open(fileName, 'r') as file:
            responseText = file.read()

    else:
        responseText = "{"
        for fixtureId in fixtureIds:
            responseText = responseText + "\"" + fixtureId + "\"" + ":"
            response = requests.get("https://api-football-v1.p.mashape.com/odds/" + str(fixtureId),
                                    headers={
                                        "X-Mashape-Key": mashapeKey,
                                        "Accept": "application/json"
                                    }
                                    )
            temp = str(response.text)
            responseText = responseText + temp + ','

    responseText = responseText.replace("\\u00e9", "e")
    responseText = responseText[:-1] + "}"
    writeResponseToFile(fileName, responseText)

    cleanOdds(json.loads(responseText))


def cleanOdds(data):
    cleanedOdds = {}

    keys = data.keys()
    newDict = {}
    for key in keys:

        innerDict = {key: "{}"}
        temp = {}
        newDict.update(innerDict)

        markets = data[key]["api"]["odds"]
        for odd in markets:
            if odd == "Result & The 2 teams score":
                market = markets[odd]
                bets = list(market.keys())
                fixedBets = ["1 / Yes", "1 / No", "N / Yes", "N / No", "2 / Yes", "2 / No"]

                for i in range(0, 6):
                    position = int(market[bets[i]]['pos']) - 1
                    market[fixedBets[position]] = market.pop(bets[i])

            if odd in requiredOdds:
                temp2 = {odd: markets[odd]}
                temp.update(temp2)
                innerDict.update({key: temp})

                newDict.update(innerDict)
                cleanedOdds = newDict

    jsonString = "{"
    for i in cleanedOdds:
        jsonString = jsonString + "\"" + i + "\":" + str(cleanedOdds[i]) + ","
    jsonString = jsonString[:-1] + "}"
    jsonString = json.loads(jsonString.replace("'", "\"").replace('None', '"NULL"'))

    writeOddsToCSV(jsonString)
    return jsonString


# leagueID = getEPLleagueID()
fixtures = getFixtures("2")
fixtures = fixtures.replace("\'", "\"").replace('None', '"NULL"')
jsonFixtures = json.loads(fixtures)
fixtureIds = []
for fixture in jsonFixtures:
    fixtureIds.append(jsonFixtures[fixture]["fixture_id"])

getOdds(fixtureIds)
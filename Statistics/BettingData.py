import json
import csv
import requests
from decimal import Decimal

isTest = False
currentGameweek = 22
requiredOdds = {"Win the match", "Both teams score", "Result & The 2 teams score", "Scorer"}
mashapeKey = "trr4b4xsHumshQ6nTWYhZnzZEdUnp1VvuQEjsnes6a8aaI5vgr"


def writeResponseToFile(fileName, text):
    """
    Store API-Football response to file

    """

    file = open(fileName, 'w')
    file.write(text)
    file.close


def writeOddsToCSV(data):
    """
    Main odds -> CSV helper function
    1. Get fixture ID, Names
    2. Get marketType
    3. Write to CSV in market-specific method

    """

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
    """
    Convert decimal odds to percentage probability

    """
    return round((1 / Decimal(odd)) * 100, 2)


def calculateFinalProbability(odds):
    """
    Return percentage probability equivalent of decimal odds
    after removing bookies cut

    :param odds: List of all odds in market per fixture
    :return: List of updated percentage probabilities
    """
    total = 0
    probabilities = []
    for odd in odds:
        probability = (1 / Decimal(odd)) * 100
        total = total + probability
        probabilities.append(probability)

    total = total - 100
    divider = total / len(odds)
    update = []
    for probability in probabilities:
        probability = round(probability - divider, 2)
        update.append(probability)

    return update


def BothTeamsScoreCSV(w, fixtureId, teams, data, isFirst):
    """
    BothTeamsToScore market specific CSV Writer method

    :param w: CSV writer
    :param fixtureId: fixtureID
    :param teams: [Team1, Team2]
    :param data: Odds
    :param isFirst: boolean value to determine whether headers should be written
    :return:
    """

    if isFirst:
        header = ['FixtureID', 'Team1', 'Team2', 'Yes', '%Yes', 'No', '%No']
        w.writerow(header)
    probabilities = calculateFinalProbability([data['Yes']['odd'], data['No']['odd']])
    content = [fixtureId, teams[0], teams[1],
               data['Yes']['odd'], probabilities[0],
               data['No']['odd'], probabilities[1]]
    w.writerow(content)


def ResultAndThe2TeamsScoreCSV(w, fixtureId, teams, data, isFirst):
    """
    ResultAndThe2TeamsScore market specific CSV Writer method

    :param w: CSV writer
    :param fixtureId: fixtureID
    :param teams: [Team1, Team2]
    :param data: Odds
    :param isFirst: boolean value to determine whether headers should be written
    :return:
    """

    if isFirst:
        header = ['FixtureID', 'Team1', 'Team2', '1 & No', '%1 & No', '1 & Yes', '%1 & Yes', '2 & No', '%2 & No',
                  '2 & Yes', '%2 & Yes', 'N & No', '%N & No', 'N & Yes', '%N & Yes']
        w.writerow(header)

    probabilities = calculateFinalProbability([data['1 / No']['odd'], data['1 / Yes']['odd'],
                                               data['2 / No']['odd'], data['2 / Yes']['odd'],
                                               data['N / No']['odd'], data['N / Yes']['odd']])

    content = [fixtureId, teams[0], teams[1], data['1 / No']['odd'], probabilities[0], data['1 / Yes']['odd'],
               probabilities[1], data['2 / No']['odd'], probabilities[2], data['2 / Yes']['odd'], probabilities[3],
               data['N / No']['odd'], probabilities[4], data['N / Yes']['odd'], probabilities[5]]
    w.writerow(content)


def WinTheMatchCSV(w, fixtureId, teams, data, isFirst):
    """
    WinTheMatch market specific CSV Writer method

    :param w: CSV writer
    :param fixtureId: fixtureID
    :param teams: [Team1, Team2]
    :param data: Odds
    :param isFirst: boolean value to determine whether headers should be written
    :return:
    """

    if isFirst:
        header = ['FixtureID', 'Team1', 'Team2', '1', '%1', 'N', '%N', '2', '%2']
        w.writerow(header)
    probabilities = calculateFinalProbability([data['1']['odd'], data['N']['odd'], data['2']['odd']])
    content = [fixtureId, teams[0], teams[1], data['1']['odd'], probabilities[0],
               data['N']['odd'], probabilities[1], data['2']['odd'], probabilities[2]]
    w.writerow(content)


def getEPLleagueID():
    """
    Constant - Returns EPL LeagueID

    :return: EPL LeagueID
    """
    fileName = 'CachedJson/getLeagues.txt'
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
    """
    Returns list of all teams playing in given League

    :param leagueID: 2 -EPL
    :return: List of teams in league
    """
    fileName = 'CachedJson/getTeams.txt'
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
    """
    Gets list of fixtures in a league given global Gameweek var

    :param leagueID: League ID
    :return: list of fixture details
    """

    fileName = "CachedJson/getFixtures.txt"
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
    """
    Given list of all fixtures in EPL, remove all that are not
    in the next Gameweek
    :param data: List of all fixtures obtained from getFixtures
    :return: Fixtures only in next Gameweek
    """
    cleanedFixtures = "{"
    for fixture in data:
        current = data[fixture]['round']
        if current == ("Premier League - " + str(currentGameweek)):
            cleanedFixtures = cleanedFixtures + "\"" + fixture + "\":" + str(data[fixture]) + ","

    cleanedFixtures = cleanedFixtures[:-1] + "}"
    cleanedFixtures = cleanedFixtures.replace("'penalty': None,", "")

    file = open("CachedJson/getCleanedFixtures.txt", 'w')
    file.write(cleanedFixtures)
    file.close
    return cleanedFixtures


def getFixtureNames():
    """
    Converts fixtureId -> Fixture teams
    :return: list of triples [fixtureID, Team1, Team2]
    """
    with open('CachedJson/getCleanedFixtures.txt', 'r') as f:
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
    """
    Returns teams playing in given FixtureID

    :param fixturesList: list of triples [fixtureID, Team1, Team2]
                            for games next gameweek.
    :param fixtureId: FixtureID needed
    :return: [Team1, Team2]
    """
    for fixture in fixturesList:
        if fixture[0] == fixtureId:
            return (fixture[1], fixture[2])


def getOdds(fixtureIds):
    """

    :param fixtureIds: List of fixtureIDs
    :return: returns list of odds per fixture
    """
    fileName = "CachedJson/getOdds.txt"
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
    """
    Remove redundant markets

    :param data: all odds
    :return: required odds
    """

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

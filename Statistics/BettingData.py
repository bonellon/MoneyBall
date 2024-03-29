import json
import csv
import requests
from decimal import Decimal

isTest = False
currentGameweek = 3
leagueID = 524
requiredOdds = {"Win the match", "Both teams score", "Results/Both Teams Score", "Scorer"}
mashapeKey = "c0fce7377emsh4084b4f22dbc8f0p17508ajsn635090a150d6"


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
            marketTitle = marketTitle.replace("/", "")

            import os

            current = os.path.abspath(os.curdir).split('\\')

            if current[len(current) - 1] == 'Historical':
                fileName = "../odds/" + marketTitle + ".csv"
            else:
                fileName = "odds/" + marketTitle + ".csv"



            if (isFirst):
                f = open(fileName, 'w+', newline='')
            else:
                f = open(fileName, 'a', newline='')

            w = csv.writer(f)
            if marketTitle == "WinTheMatch":
                WinTheMatchCSV(w, fixtureId, teams, data[fixtureId][market], isFirst)
            elif marketTitle == "BothTeamsScore":
                BothTeamsScoreCSV(w, fixtureId, teams, data[fixtureId][market], isFirst)
            elif marketTitle == "ResultsBothTeamsScore":
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

    dataList = {}
    for i in data:
        temp = {i['value']:i['odd']}
        dataList.update(temp)
    data = dataList

    if isFirst:
        header = ['FixtureID', 'Team1', 'Team2', '1 & No', '%1 & No', '1 & Yes', '%1 & Yes', '2 & No', '%2 & No',
                  '2 & Yes', '%2 & Yes', 'N & No', '%N & No', 'N & Yes', '%N & Yes']
        w.writerow(header)

    probabilities = calculateFinalProbability([data['Home/No'], data['Home/Yes'],
                                               data['Away/No'], data['Away/Yes'],
                                               data['Draw/No'], data['Draw/Yes']])

    try:
        content = [fixtureId, teams[0], teams[1], data['Home/No'], probabilities[0], data['Home/Yes'],
                   probabilities[1], data['Away/No'], probabilities[2], data['Away/Yes'], probabilities[3],
                   data['Draw/No'], probabilities[4], data['Draw/Yes'], probabilities[5]]
        w.writerow(content)
    except:
        print("Error")

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
def getTeams():
    """
    Returns list of all teams playing in given League

    :param leagueID: 524 -EPL
    :return: List of teams in league
    """
    fileName = 'CachedJson/getTeams.txt'
    if isTest:
        with open(fileName, 'r') as file:
            responseText = file.read()

    else:
        response = requests.get("https://api-football-v1.p.mashape.com/teams/league/" + leagueID,
                                headers={
                                    "X-RapidAPI-Key": mashapeKey,
                                    "Accept": "application/json"
                                }
                                )
        responseText = response.text
        writeResponseToFile(fileName, responseText)

    data = json.loads(responseText)
    return data['api']['teams']


# get list of next gameweek fixtures
def getFixtures(leagueID, gw):
    """
    Gets list of fixtures in a league given global Gameweek var

    :param leagueID: League ID
    :return: list of fixture details
    """
    import os
    from pathlib import Path

    filePath = str(Path(__file__).parents[1])+"\\Statistics\\CachedJson\\getFixtures.txt"

    if os.path.isfile(filePath) and os.stat(filePath).st_size != 0:
        with open(filePath, 'r') as file:
            responseText = file.read()

    else:

        response = requests.get("https://api-football-v1.p.mashape.com/fixtures/league/" + str(leagueID),
                                headers={
                                    "X-Mashape-Key": mashapeKey,
                                    "Accept": "application/json"
                                }
                                )
        responseText = response.text

    data = json.loads(responseText)["api"]["fixtures"]
    writeResponseToFile(filePath, responseText)
    return cleanFixtureFile(data, gw)


def cleanFixtureFile(data, gw):
    """
    Given list of all fixtures in EPL, remove all that are not
    in the next Gameweek
    :param data: List of all fixtures obtained from getFixtures
    :return: Fixtures only in next Gameweek
    """
    cleanedFixtures = "{"
    for fixture in data:
        current = data[fixture]['round']
        if current == ("Regular Season - "+str(gw)):
            cleanedFixtures = cleanedFixtures + "\"" + fixture + "\":" + str(data[fixture]) + ","

    cleanedFixtures = cleanedFixtures[:-1] + "}"
    cleanedFixtures = cleanedFixtures.replace("'penalty': None,", "")

    import os

    current = os.path.abspath(os.curdir).split('\\')
    if current[len(current)-1] == 'Historical':
        file = open("../CachedJson/getCleanedFixtures.txt", 'w')
    else:
        file = open("CachedJson/getCleanedFixtures.txt", 'w')
    file.write(cleanedFixtures)
    file.close
    return cleanedFixtures


def getFixtureNames():
    """
    Converts fixtureId -> Fixture teams
    :return: list of triples [fixtureID, Team1, Team2]
    """
    import os
    current = os.path.abspath(os.curdir).split('\\')
    if current[len(current) - 1] == 'Historical':
        file = open("../CachedJson/getCleanedFixtures.txt", 'r')
    else:
        file = open('CachedJson/getCleanedFixtures.txt', 'r')

    read = file.read()
    jsonFixtures = json.loads(read.replace("'", "\"").replace('None', '"NULL"'))

    fixturesList = []
    for fixture in jsonFixtures:
        fixtureId = jsonFixtures[fixture]['fixture_id']
        homeTeam = jsonFixtures[fixture]['homeTeam']
        awayTeam = jsonFixtures[fixture]['awayTeam']

        fixture = [fixtureId, homeTeam, awayTeam]
        fixturesList.append(fixture)

    file.close
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

    return "ERROR!"


def getOdds(fixtureIds):
    """

    :param fixtureIds: List of fixtureIDs
    :return: returns list of odds per fixture
    """
    import os
    current = os.path.abspath(os.curdir).split('\\')
    if current[len(current)-1] == 'Historical':
        fileName = "../CachedJson/getOdds.txt"
    else:
        fileName = "CachedJson/getOdds.txt"

    if isTest:
        with open(fileName, 'r') as file:
            responseText = file.read()

    else:
        responseText = "{"
        for fixtureId in fixtureIds:
            responseText = responseText + "\"" + fixtureId + "\"" + ":"

            url = "https://api-football-v1.p.rapidapi.com/v2/odds/fixture/"

            response = requests.get(url + str(fixtureId),
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

    return cleanOdds(json.loads(responseText))


def cleanOdds(data):
    """
    Remove redundant markets

    :param data: all odds
    :return: required odds
    """

    cleanedOdds = {}

    keys = data.keys()
    newDict = {}

    try:
        for key in keys:

            innerDict = {key: "{}"}
            temp = {}
            newDict.update(innerDict)

            bookies = data[key]["api"]["odds"][0]["bookmakers"]

            for bookie in bookies:
                if bookie["bookmaker_name"] == "Bet365":
                    brand = bookie


            markets = brand["bets"]
            for odd in markets:
                if odd['label_name'] == "Results/Both Teams Score":
                    market = odd
                    bets = list(market.keys())
                    fixedBets = ["Home/Yes", "Home/No", "Draw/Yes", "Draw/No", "Away/Yes", "Away/No"]

        #No idea what the point of this was? Possibly just testing to make sure all odds exist???
                    #for i in range(0, 6):
                    #    position = int(market["values"[i]]['odd']) - 1
                    #    market[fixedBets[position]] = market.pop(bets[i])

                if odd['label_name'] in requiredOdds:
                    temp2 = {odd['label_name']: odd['values']}
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

    except:
        print("IDEK...")


def getOddsGW(gw):
    # leagueID = getEPLleagueID()
    fixtures = getFixtures(leagueID, gw)
    fixtures = fixtures.replace("\'", "\"").replace('None', '"NULL"')
    jsonFixtures = json.loads(fixtures)
    fixtureIds = []
    for fixture in jsonFixtures:
        fixtureIds.append(jsonFixtures[fixture]["fixture_id"])

    odds = getOdds(fixtureIds)
    return odds;

'''
# leagueID = getEPLleagueID()
fixtures = getFixtures("2", currentGameweek)
fixtures = fixtures.replace("\'", "\"").replace('None', '"NULL"')
jsonFixtures = json.loads(fixtures)
fixtureIds = []
for fixture in jsonFixtures:
    fixtureIds.append(jsonFixtures[fixture]["fixture_id"])

getOdds(fixtureIds)
'''
getOddsGW(currentGameweek)


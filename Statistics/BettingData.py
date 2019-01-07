import json
import csv
import requests

isTest = True
currentGameweek = 19
requiredOdds = {"Win the match", "Both teams score", "Result & The 2 teams score", "Scorer"}
mashapeKey = "trr4b4xsHumshQ6nTWYhZnzZEdUnp1VvuQEjsnes6a8aaI5vgr"


def writeResponseToFile(fileName, text):
    file = open(fileName, 'w')
    file.write(text)
    file.close


def writeOddsToCSV2(data):
    isFirst = True
    for fixture in data:
        for market in data[fixture]:
            marketTitle = market.title().replace(" ", "")
            fileName = "odds/" + marketTitle + ".csv"
            if(isFirst):
                f = open(fileName, 'w', newline='')
            else:
                f = open(fileName, 'a', newline='')

            w = csv.writer(f)
            if marketTitle == "WinTheMatch":
                WinTheMatchCSV(w, fixture, data[fixture][market], isFirst)
            elif marketTitle == "BothTeamsScore":
                BothTeamsScoreCSV(w, fixture, data[fixture][market], isFirst)
            elif marketTitle == "Result&The2TeamsScore":
                ResultAndThe2TeamsScoreCSV(w, fixture, data[fixture][market], isFirst)
            f.close()
        isFirst = False


def writeOddsToCSV(fixtureId, odds):
    for market in odds:
        marketTitle = market.title().replace(" ", "")
        fileName = "odds/" + marketTitle + ".csv"
        f = open(fileName, 'w', newline='')
        w = csv.writer(f)
        if marketTitle == "WinTheMatch":
            WinTheMatchCSV(w, fixtureId, odds[market])
        elif marketTitle == "BothTeamsScore":
            BothTeamsScoreCSV(w, fixtureId, odds[market])
        #elif marketTitle == "Result&The2TeamsScore":
            #ResultAndThe2TeamsScoreCSV(w, fixtureId, odds[market])
        f.close()


def BothTeamsScoreCSV(w, fixtureId, data, isFirst):
    if isFirst:
        header = ['FixtureID', 'Yes', 'No']
        w.writerow(header)
    content = [fixtureId, data['Yes']['odd'], data['No']['odd']]
    w.writerow(content)


def ResultAndThe2TeamsScoreCSV(w, fixtureId, data, isFirst):
    if isFirst:
        header = ['FixtureID', '1 & No', '1 & Yes', '2 & No', '2 & Yes', 'N & No', 'N & Yes']
        w.writerow(header)
    content = [fixtureId, data['1 / No']['odd'], data['1 / Yes']['odd'], data['2 / No']['odd'], data['2 / Yes']['odd'],
               data['N / No']['odd'], data['N / Yes']['odd']]
    w.writerow(content)


def WinTheMatchCSV(w, fixtureId, data, isFirst):
    if isFirst:
        header = ['FixtureID', '1', 'N', '2']
        w.writerow(header)
    content = [fixtureId, data['1']['odd'], data['N']['odd'], data['2']['odd']]
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
                                    "X-Mashape-Key": "trr4b4xsHumshQ6nTWYhZnzZEdUnp1VvuQEjsnes6a8aaI5vgr",
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
            cleanedFixtures = cleanedFixtures + "\""+fixture+"\":" + str(data[fixture])+","

    cleanedFixtures = cleanedFixtures[:-1] +"}"
    cleanedFixtures = cleanedFixtures.replace("'penalty': None,", "")

    file = open("getCleanedFixtures.txt", 'w')
    file.write(cleanedFixtures)
    file.close
    return cleanedFixtures


def getOdds(fixtureIds):
    fileName = "getOdds.txt"
    if isTest:
        with open(fileName, 'r') as file:
            responseText = file.read()

    else:
        responseText = "{"
        for fixtureId in fixtureIds:
            responseText = responseText + "\"" + fixtureId + "\"" +":"
            response = requests.get("https://api-football-v1.p.mashape.com/odds/" + str(fixtureId),
                                    headers={
                                        "X-Mashape-Key": "trr4b4xsHumshQ6nTWYhZnzZEdUnp1VvuQEjsnes6a8aaI5vgr",
                                        "Accept": "application/json"
                                    }
                                    )
            temp = str(response.text)
            #temp = temp[1:-1]
            responseText = responseText + temp + ','

    responseText = responseText.replace("\\u00e9", "e")
    responseText = responseText[:-1]
    responseText = responseText+'}'
    writeResponseToFile(fileName, responseText)

    #data = json.loads(responseText)["api"]["odds"]
    #return cleanOdds(fixtureIds, data)
    cleanOdds2(json.loads(responseText))

def cleanOdds2(data):
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
                    position = int(market[bets[i]]['pos'])-1
                    market[fixedBets[position]] = market.pop(bets[i])

            if odd in requiredOdds:
                #newDict.update({key:{odd: "{}"}})
                temp2 = {odd: markets[odd]}
                temp.update(temp2)
                innerDict.update({key: temp})

                newDict.update(innerDict)
                #newDict[key][odd] = markets[odd]
                cleanedOdds = newDict
                #cleanedOdds[odd] = markets[odd]
    jsonString = "{"
    for i in cleanedOdds:
        jsonString = jsonString + "\"" + i+ "\":"
        jsonString = jsonString + str(cleanedOdds[i]) + ","
    jsonString = jsonString[:-1]+"}"
    print(jsonString)
    jsonString = json.loads(jsonString.replace("'", "\""))
    writeOddsToCSV2(jsonString)
    return jsonString

def cleanOdds(fixtureId, odds):
    cleanedOdds = {}
    for odd in odds:
        if odd == "Result & The 2 teams score":
            market = odds[odd]
            bets = list(market.keys())
            fixedBets = ["1 / Yes", "1 / No", "N / Yes", "N / No", "2 / Yes", "2 / No"]

            for i in range(1, 6):
                position = market[bets[i]]['pos']
                market[fixedBets[int(position) - 1]] = market.pop(bets[i])

        if odd in requiredOdds:
            cleanedOdds[odd] = odds[odd]
    writeOddsToCSV(fixtureId, cleanedOdds)
    return cleanedOdds


# leagueID = getEPLleagueID()
fixtures = getFixtures("2")
jsonFixtures = json.loads(fixtures.replace("\'", "\""))
fixtureIds = []
for fixture in jsonFixtures:
    fixtureIds.append(jsonFixtures[fixture]["fixture_id"])

getOdds(fixtureIds)

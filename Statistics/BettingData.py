import json
import requests

mashapeKey = "trr4b4xsHumshQ6nTWYhZnzZEdUnp1VvuQEjsnes6a8aaI5vgr"


def getEPLleagueID():
    response = requests.get("https://api-football-v1.p.mashape.com/leagues",
                            headers={
                                "X-Mashape-Key": mashapeKey,
                                "Accept": "application/json"
                            }
                            )
    test = json.loads(response.text)
    leagues2 = test['api']['leagues']
    league_id = 0

    for i in leagues2:
        league_name = leagues2[i]['name']
        league_country = leagues2[i]['country']
        league_season = leagues2[i]['season']
        if league_name == "Premier League" and league_country == "England" and league_season == "2018":
            league_id = i
            break
    return league_id


# get list of teams in league
def getTeams(leagueID):
    response = requests.get("https://api-football-v1.p.mashape.com/teams/league/" + leagueID,
                            headers={
                                "X-Mashape-Key": mashapeKey,
                                "Accept": "application/json"
                            }
                            )

    data = json.loads(response.content)
    teams = data['api']['teams']
    return teams


# get League data
# English Premier League =  2
leagueID = getEPLleagueID()
teams = getTeams(leagueID)

# get list of next gameweek fixtures

# for each game in next gameweek; get odds

# store odds per fixture in csv

import json

import requests

mashapeKey = "trr4b4xsHumshQ6nTWYhZnzZEdUnp1VvuQEjsnes6a8aaI5vgr"

# get League data
# English Premier League =  2

response = requests.get("https://api-football-v1.p.mashape.com/leagues",

                        headers={
                            "X-Mashape-Key": mashapeKey,
                            "Accept": "application/json"
                        }
                        )
test = json.loads(response.text)
leagues = test
leagues2 = test['leagues']
leagueID = 2

#get list of teams in league
response = requests.get("https://api-football-v1.p.mashape.com/teams/league/2",
  headers={
    "X-Mashape-Key": mashapeKey,
    "Accept": "application/json"
  }
)

data = json.loads(response.content)
print(data.api.teams)


# get list of next gameweek fixtures

# for each game in next gameweek; get odds

# store odds per fixture in csv

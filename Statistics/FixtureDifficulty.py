'''
Pull table from https://premierfantasytools.com/fpl-fixture-difficulty/#1543979080316-5874f1a6-1bb3
'''

# Import the libraries we need
import pandas as pd
from Statistics.fpl import getTeamIds


#def convertToTeam():


attackURL = "https://premierfantasytools.com/fpl-fixture-difficulty/#1543979080334-134ad6be-5480"
defenseURL = 'https://premierfantasytools.com/fpl-fixture-difficulty/#1543979080316-5874f1a6-1bb3'
tables = pd.read_html(attackURL, encoding='utf-8')

attack = tables[0]
attack.head(10)
attack.rename(columns={'Unnamed: 0': 'teams'}, inplace=True)

def convertToShortTeamName(teamName):
    return teamName[:-1]

gw25 = attack.iloc[:, 0:2]
gw25['teams'] = gw25['teams'].apply(convertToShortTeamName)
print(gw25)

attackDict = {}
for row in gw25.iterrows():
    temp = {}
    index, data = row
    current = data.tolist()
    temp = {current[0]:current[1]}
    attackDict.update(temp)

teams = getTeamIds()

for team in teams:
    current = teams[team]
    current.update({"opponent":attackDict[team]})


print(teams)





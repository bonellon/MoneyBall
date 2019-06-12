import os
import pandas as pd
import Blogs.combinator as cb
import Blogs.AylienAPI as aylien
import Blogs.blog_injury as injury

from googlesearch import search

currentGW = 38

def googleSearch():

    query = 'Fantasy Premier League gameweek "'+str(currentGW)+'"'
    urls = []
    print(query)
    for url in search(query, stop=300, pause=2.0, tbs="qdr:y"):
        print("Appending: "+str(len(urls)))
        urls.append(url)

    query = 'FPL gameweek '+str(currentGW)

    print(query)
    for url in search(query, stop=300, pause=2.0, tbs="qdr:y"):
        if url not in urls:
            print("Appending: "+str(len(urls)))
            urls.append(url)

    query = 'FPL budget gameweek ' + str(currentGW)


    print(query)
    for url in search(query, stop=50, pause=1.0, tbs="qdr:y"):
        if url not in urls:
            print("Appending: " + str(len(urls)))
            urls.append(url)

    query = 'FPL injury gameweek ' + str(currentGW)
    for url in search(query, stop=50, pause=1.0, tbs="qdr:y"):
        if url not in urls:
            print("Appending: " + str(len(urls)))
            urls.append(url)

    with open('urls.txt', 'w') as f:
        for item in urls:
            f.write("%s\n" % item)


def iterateBlogs():


    if not os.path.isfile('urls.txt'):
        googleSearch()

    with open("urls.txt", 'r') as f:
        urls = f.read().splitlines()

    resultList= list(result)
    try:
        currentLatest = int(resultList[len(resultList) - 1])
    except:
        currentLatest = 0

    for i in range(currentLatest, len(urls)):
        getRatings(urls[i], players, str(i))
        players.to_csv("playersResult.csv")

    getTotalRatings(players)
    print(players.head())

    print("Removing injured players...")
    removeInjuries()

    sortByElementID(players)
    players.to_csv("playersResult.csv")


def sortByElementID(allPlayers):
    keeper = allPlayers.drop(allPlayers[allPlayers.elementID != 1].index)
    keeper.sort_values("score", inplace=True, ascending=False)
    print("Goalkeepers: ")
    print(keeper.head(2))

    defender = allPlayers.drop(allPlayers[allPlayers.elementID != 2].index)
    defender.sort_values("score", inplace=True, ascending=False)
    print("Defenders: ")
    print(defender.head(6))

    midfielder = allPlayers.drop(allPlayers[allPlayers.elementID != 3].index)
    midfielder.sort_values("score", inplace=True, ascending=False)
    print("Midfielders: ")
    print(midfielder.head(6))

    forward = allPlayers.drop(allPlayers[allPlayers.elementID != 4].index)
    forward.sort_values("score", inplace=True, ascending=False)
    print("Forwards: ")
    print(forward.head(3))


def removeInjuries():

    injuries = injury.main()
    for index, row in players.iterrows():
        for index2, row2 in injuries.iterrows():
            if row["secondName"] == row2["secondName"]:
                print("Injured: "+row["secondName"])
                players.set_value(index, "score", row["score"]-1.00)



def getRatings(url, players, blogCount):
    print("Analysing "+str(blogCount)+"\n")
    json = aylien.getRatings(url)

    players[blogCount] = pd.Series(0.00, index=players.index)

    #Exceptions return None - No internet, url is image/video etc.
    if json == None:
        return

    for entity in json['entities']:
        name = entity['mentions'][0]["text"]
        sentiment = entity['overall_sentiment']

        matchName(name, sentiment, players, str(blogCount))

def getTotalRatings(players):
    columns = []
    for col in players:
        if col.isdigit():
            columns.append(col)

    players["score"] = players[columns].sum(axis =1)
    players.sort_values("score", inplace=True)



def matchName(name, sentiment, players, blogCounter):
    for index, row in players.iterrows():
        if(name in row["fullName"] or row["secondName"] in name or name in row['cleanName']):
            print("\tMATCHED! : "+name + "  -  "+row['fullName'])
            sentimentScore = getSentiment(sentiment)
            players.set_value(index, blogCounter, row[blogCounter]+sentimentScore)
            return

def getSentiment(sentiment):
    confidence = sentiment["confidence"]
    polarity = sentiment["polarity"]

    if polarity == "positive":
        return confidence+1.00
    elif polarity == "neutral":
        return confidence
    return confidence-1.00

if __name__ == '__main__':
    blogs = pd.read_csv("blogs.csv", delimiter=',', sep='\n')
    players = pd.read_csv("players.csv", delimiter=',', sep='\n')

    if os.path.isfile('urls.txt'):
        result = pd.read_csv("playersResult.csv", delimiter=',', sep='\n')

    iterateBlogs()

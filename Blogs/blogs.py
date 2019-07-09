import os
import pandas as pd
import Blogs.combinator as cb
import Blogs.AylienAPI as aylien
import Blogs.blog_injury as injury

from googlesearch import search

def googleSearch(currentGW):

    query = 'Fantasy Premier League gameweek "'+str(currentGW)+'"'
    urls = []
    print(query)
    for url in search(query, stop=100, pause=2.0, tbs="qdr:y"):
        print("Appending: "+str(len(urls)))
        urls.append(url)
    '
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
    '
    with open('urls.txt', 'w') as f:
        for item in urls:
            f.write("%s\n" % item)


def iterateBlogs(players):

    try:
        resultList = list(players)
        currentLatest = int(str(resultList[len(resultList) - 1]).split("_")[1])+1
    except:
        currentLatest = 1

    for currentGW in range(currentLatest,39):

        players["score_"+str(currentGW)] = pd.Series(0.00, index=players.index)

        googleSearch(currentGW)

        with open("urls.txt", 'r') as f:
            urls = f.read().splitlines()


        for i in range(0, len(urls)):
            getRatings(urls[i], players, str(i), currentGW)
            players.to_csv("playersResult.csv")

        print(players.head())

        print("Removing injured players...")
        removeInjuries(currentGW,players)

        #sortByElementID(players)
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


def removeInjuries(currentGW, players):

    injuries = injury.main()
    for index, row in players.iterrows():
        for index2, row2 in injuries.iterrows():
            if row["secondName"] == row2["secondName"]:
                players.set_value(index, "score_"+str(currentGW), row["score_"+str(currentGW)]-1.00)



def getRatings(url, players, blogCount, currentGW):
    print("Analysing "+str(blogCount)+"\n")
    json = aylien.getRatings(url)

    #Exceptions return None - No internet, url is image/video etc.
    if json == None:
        return

    for entity in json['entities']:
        name = entity['mentions'][0]["text"]
        sentiment = entity['overall_sentiment']

        matchName(name, sentiment, players, currentGW)


def matchName(name, sentiment, players, currentGW):
    for index, row in players.iterrows():
        if(name in row["fullName"] or row["secondName"] in name or name in row['cleanName']):
            try:
                print("\tMATCHED! : "+name + "  -  "+row['fullName'])
            except:
                print("\tMATCHED!" +row['fullName'])

            sentimentScore = getSentiment(sentiment)
            players.set_value(index, "score_"+str(currentGW), row["score_"+str(currentGW)]+sentimentScore)
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

    if os.path.isfile('playersResult.csv'):
        players = pd.read_csv("playersResult.csv", delimiter=',', sep='\n')
    else:
        players = pd.read_csv("players.csv", delimiter=',', sep='\n')

    iterateBlogs(players)

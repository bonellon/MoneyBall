import pandas as pd
import Blogs.combinator as cb
import Blogs.AylienAPI as aylien

from googlesearch import search

currentGW = 38

def googleSearch():

    query = 'Fantasy Premier League gameweek "'+str(currentGW)+'"'
    urls = []
    print(query)
    for url in search(query, stop=500, pause=1.0, tbs="qdr:y"):
        print("Appending: "+str(len(urls)))
        urls.append(url)

    query = 'FPL gameweek '+str(currentGW)

    print(query)
    for url in search(query, stop=300, pause=1.0, tbs="qdr:y"):
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

    for i in range(0, len(urls)):
        getRatings(urls[i], players, str(i))
        players.to_csv("playersResult.csv")

    getTotalRatings(players)
    print(players.head())
    players.to_csv("playersResult.csv")

def iterateBlogs():
    for index, row in blogs.iterrows():
        url = row["URL"]
        change = row["Change"]

        url = url.replace(str(change), str(currentGW))

        getRatings(url, players, str(index))

    getTotalRatings(players)
    print(players.head())
    players.to_csv("playersResult.csv")


def getRatings(url, players, blogCount):
    print("Analysing "+str(blogCount)+"\n")
    json = aylien.getRatings(url)

    players[blogCount] = pd.Series(0.00, index=players.index)

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
            players.set_value(index, blogCounter, sentimentScore)
            return

def getSentiment(sentiment):
    confidence = sentiment["confidence"]
    polarity = sentiment["polarity"]

    if polarity == "positive":
        return confidence+1.00
    elif polarity == "neutral":
        return confidence
    return confidence-1.00


blogs = pd.read_csv("blogs.csv", delimiter=',', sep='\n')
players = pd.read_csv("players.csv", delimiter=',', sep='\n')

#iterateBlogs()
googleSearch()

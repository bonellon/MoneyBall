import pandas as pd
import Blogs.combinator as cb
import Blogs.AylienAPI as aylien

currentGW = 38

def iterateBlogs():
    blogs = pd.read_csv("blogs.csv", delimiter=',', sep='\n')
    players = pd.read_csv("players.csv", delimiter=',', sep='\n')

    for index, row in blogs.iterrows():
        url = row["URL"]
        change = row["Change"]

        url = url.replace(str(change), str(currentGW))

        getRatings(url, players, str(index))

    getTotalRatings(players)
    print(players.head())
    players.to_csv("playersResult.csv")


def getRatings(url, players, blogCount):
    json = aylien.getRatings(url)

    players[blogCount] = pd.Series(0.00, index=players.index)

    for entity in json['entities']:
        name = entity['mentions'][0]["text"]
        sentiment = entity['overall_sentiment']

        print(name+" : "+sentiment["polarity"]+". Confidence: "+str(sentiment["confidence"]))
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
            print("MATCHED! : "+name + "  -  "+row['fullName'])
            sentimentScore = getSentiment(sentiment)
            players.set_value(index, blogCounter, sentimentScore)
            return
    print("No match found for : " + name)

def getSentiment(sentiment):
    confidence = sentiment["confidence"]
    polarity = sentiment["polarity"]

    if polarity == "positive":
        return confidence+1.00
    elif polarity == "neutral":
        return confidence
    return confidence-1.00

iterateBlogs()
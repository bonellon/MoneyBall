'''
Main class for Blogs + News articles
Contains combination methods + general methods used for all blogs
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import csv


def getContents(url):
    page = requests.get(url)
    content = page.content

    return BeautifulSoup(content, features="lxml")


def getPlayerCSV():
    return pd.read_csv("players.csv")


def createPlayerCSV(url):
    r = requests.get(url)
    data = json.loads(r.text)

    all_players = data['elements']
    dataset = []
    for player in all_players:
        current = {"webName": player['web_name'],
                   "ID": player['id'],
                   "firstName":player['first_name'],
                   "secondName":player['second_name'],
                   "fullName": player['first_name']
                           + " " + player["second_name"]}
        dataset.append(current)

    with open("players.csv", 'w',encoding='utf-8-sig') as out:
        dict_writer = csv.DictWriter(out,dataset[0].keys(), lineterminator = '\n')
        dict_writer.writeheader()
        dict_writer.writerows(dataset)
    return all_players


url = "https://fantasy.premierleague.com/drf/bootstrap-static"
createPlayerCSV(url)

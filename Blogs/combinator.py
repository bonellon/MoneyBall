'''
Main class for Blogs + News articles
Contains combination methods + general methods used for all blogs
'''

import requests
import pandas as pd
import json
import csv
import os
import string

from bs4 import BeautifulSoup
from unidecode import unidecode


def getContents(url):
    page = requests.get(url)
    content = page.content

    return BeautifulSoup(content, features="lxml")


def getPlayerCSV():
    return pd.read_csv("players.csv")


def createPlayerCSV(url):
    if os.path.isfile('players.csv') and os.stat("players.csv").st_size != 0:
        return

    r = requests.get(url)
    data = json.loads(r.text)

    all_players = data['elements']
    dataset = []
    for player in all_players:
        current = {"webName": player['web_name'],
                   "ID": player['id'],
                   "firstName": player['first_name'],
                   "secondName": player['second_name'],
                   "fullName": player['first_name'] + " " + player["second_name"],
                   "cleanName": unidecode(player['first_name'] + " " + player["second_name"]).translate(
                       str.maketrans('', '', string.punctuation))}
        dataset.append(current)

    with open("players.csv", 'w', encoding='utf-8-sig') as out:
        dict_writer = csv.DictWriter(out, dataset[0].keys(), lineterminator='\n')
        dict_writer.writeheader()
        dict_writer.writerows(dataset)
    return all_players


FPL_url = "https://fantasy.premierleague.com/drf/bootstrap-static"
createPlayerCSV(FPL_url)

'''
1. Check injured players and remove from players array


2. Iterate through each blog in blogs.csv and give points to players corresponding to sentiment scores
'''

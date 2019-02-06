'''
Pull table from https://premierfantasytools.com/fpl-fixture-difficulty/#1543979080316-5874f1a6-1bb3
'''

# Import the libraries we need
import pandas as pd
import re
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime

def convertToTeam():


attackURL = "https://premierfantasytools.com/fpl-fixture-difficulty/#1543979080334-134ad6be-5480"
defenseURL = 'https://premierfantasytools.com/fpl-fixture-difficulty/#1543979080316-5874f1a6-1bb3'
tables = pd.read_html(attackURL, encoding='utf-8')

attack = tables[0]
attack.head(10)


gw25 = attack[['Unnamed: 0', 'GW 25']]
print(gw25)



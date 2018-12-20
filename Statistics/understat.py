import pandas as pd
import csv
from selenium import webdriver
import urllib.request

def downloadTable():
    try:
        url = 'https://understat.com/league/EPL/2018'
        driver = webdriver.PhantomJS()
        driver.get(url)
        table = driver.find_element_by_id(id_="league-chemp")

        return table

    except Exception as e:
        print("Error in download... ", e)

def getTable():
    try:

        stat_tables = pd.read_html("temp.html", encoding="utf-8")
        table1 = stat_tables[0]

    except Exception as e:
        print("Error occured", e)


tables = downloadTable()
#getTable()
print("Done!")
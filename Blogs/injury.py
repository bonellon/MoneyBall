'''
Injury table obtained from
https://www.fantasyfootballscout.co.uk/fantasy-football-injuries/
'''

import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.fantasyfootballscout.co.uk/fantasy-football-injuries/"

page = requests.get(url)
content = page.content

soup = BeautifulSoup(content)

table = soup.find("table")
table_rows = table.find_all('tr')
tb = []
for tr in table_rows:
    td = tr.find_all('td')
    row = [tr.text for tr in td]
    tb.append(row)
final = pd.DataFrame(tb, columns=["Name", "Club", "Status", "Return Date", "Latest News", "Last Updated"])
pd.head(final)

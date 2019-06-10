'''
Injury table obtained from
https://www.fantasyfootballscout.co.uk/fantasy-football-injuries/
'''

import pandas as pd
import Blogs.combinator as cb

url = "https://www.fantasyfootballscout.co.uk/fantasy-football-injuries/"
soup = cb.getContents(url)

csv = cb.getPlayerCSV()


def addFirstName(row):
    name = row['Name']
    if(name is None):
        return ""
    name = name.split('(')
    if len(name) == 1:
        return ""
    return name[1].split(')')[0].strip()

def addSecondName(row):
    name = row['Name']
    if(name is None):
        return ""
    name = name.split('(')
    return name[0].strip()


table_rows = soup.find("table").find_all('tr')
tb = []
for tr in table_rows:
    td = tr.find_all('td')
    row = [tr.text for tr in td]
    tb.append(row)
ds = pd.DataFrame(tb, columns=["Name", "Club", "Status", "Return Date", "Latest News", "Last Updated"])
ds = ds.drop(ds.index[[0]])
ds['First Name'] = ds.apply(lambda row: addFirstName(row), axis = 1)
ds['Second Name'] = ds.apply(lambda row: addSecondName(row), axis = 1)

print(ds.head())

i = 0
for index,row in ds.iterrows():
    for index2, row2 in csv.iterrows():
        print(str(row["Second Name"])+ " " +row2["secondName"])
        if row["Second Name"] == row2["secondName"]:
            i+=1

print("Total injuries matched: "+str(i)+"/"+str(index))



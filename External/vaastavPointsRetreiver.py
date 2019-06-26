import os
import pandas as pd
import csv
directory = "Vaastav//Data"

points = []

for folder in os.listdir(directory):
    subdir = directory+"//"+folder+"//gws"

    for file in os.listdir(subdir):
        if file.startswith("gw"):
            df = pd.read_csv(subdir+"//"+file, encoding = "cp1252")

            for iter, row in df.iterrows():
                print(row['total_points'])
                points.append(row['total_points'])

with open("points.csv", 'w') as csvFile:
    wr = csv.writer(csvFile, quoting=csv.QUOTE_ALL)
    wr.writerow(points)


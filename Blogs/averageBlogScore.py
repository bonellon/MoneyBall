import csv

data = list(csv.reader(open('scores.csv')))

blogs = []

for blog in data:
    for elem in blog:
        try:
            blogs.append(round(float(elem)))
        except:
            print("ERROR: "+elem)
            blogs.append(0)

with open('scoresClean.csv', 'w') as file:
    csv_writer = csv.writer(file,delimiter="\n")
    csv_writer.writerow(blogs)
import Statistics.Historical.GradientBoosting as GB
import sys
import pandas as pd

def convertToCSV(file_name, df):
    df.to_csv(file_name, encoding='utf-8')


def predictor(toRemove, csvName):
    df = pd.DataFrame(columns=columns, index=[1, 2, 3])

    for currentGW in range(2, 4):

        #toRemove = ['y', 'Player', 'BPS', 'Round', 'isCaptain', 'Points']  # ,'BlogScore', 'DefenseOdds', 'OffenceOdds']

        result = GB.main(toRemove, currentGW)
        print("Average Points = "+str(result[0]))
        print("Total Points = "+str(result[1]))

        for i in range(0, len(result[1])):
            df.at[i+1, "GW_"+str(currentGW)] = result[1][i]

    convertToCSV(csvName, df)


if __name__ == '__main__':

    args = sys.argv
    if len(args) == 1:
        remover = 0
    else:
        remover = int(sys.argv[1])


    

    columns = []
    for i in range(2, 39):
        columns.append("GW_"+str(i))




    removeAll = pd.DataFrame(columns = columns, index=[1,2,3])
    removeOdds = pd.DataFrame(columns = columns, index=[1,2,3])
    removeBlog = pd.DataFrame(columns = columns, index=[1,2,3])
    removeNone = pd.DataFrame(columns = columns, index=[1,2,3])

    for currentGW in range(2, 4):

        toRemove = ['y', 'Player', 'BPS', 'Round', 'isCaptain', 'Points']  # ,'BlogScore', 'DefenseOdds', 'OffenceOdds']

        result = GB.main(toRemove, currentGW)
        print("Average Points = "+str(result[0]))
        print("Total Points = "+str(result[1]))

        for i in range(0, len(result[1])):
            removeAll.at[i+1, "GW_"+str(currentGW)] = result[1][i]

        toRemove = ['y', 'Player', 'BPS', 'Round', 'isCaptain', 'Points','BlogScore']
        result = GB.main(toRemove, currentGW)
        print("Average Points = "+str(result[0]))
        print("Total Points = "+str(result[1]))

        for i in range(0, len(result[1])):
            removeOdds.at[i+1, "GW_"+str(currentGW)] = result[1][i]

        toRemove = ['y', 'Player', 'BPS', 'Round', 'isCaptain', 'Points', 'DefenseOdds', 'OffenceOdds']
        result = GB.main(toRemove, currentGW)
        print("Average Points = "+str(result[0]))
        print("Total Points = "+str(result[1]))

        for i in range(0, len(result[1])):
            removeBlog.at[i+1, "GW_"+str(currentGW)] = result[1][i]

        toRemove = ['y', 'Player', 'BPS', 'Round', 'isCaptain', 'Points','BlogScore', 'DefenseOdds', 'OffenceOdds']
        result = GB.main(toRemove, currentGW)
        print("Average Points = "+str(result[0]))
        print("Total Points = "+str(result[1]))

        for i in range(0, len(result[1])):
            removeNone.at[i+1, "GW_"+str(currentGW)] = result[1][i]

    convertToCSV("removeAll.csv", removeAll)
    convertToCSV("removeOdds.csv", removeOdds)
    convertToCSV("removeBlog.csv", removeBlog)
    convertToCSV("removeNone.csv", removeNone)

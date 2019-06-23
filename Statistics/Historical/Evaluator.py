import sys
import pandas as pd
import Statistics.Historical.GradientBoosting as GB


def convertToCSV(file_name, df):
    df.to_csv(file_name, encoding='utf-8')


def predictor(columns, toRemove, csvName):
    df = pd.DataFrame(columns=columns, index=[1, 2, 3])

    for currentGW in range(38, 39):

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

    if remover == 1 or remover == 0:
        predictor(columns, ['y', 'Player', 'BPS', 'Round', 'isCaptain', 'Points'],
                  "removeNone.csv")

    '''
    if remover == 2 or remover == 0:
            predictor(columns, ['y', 'Player', 'BPS', 'Round', 'isCaptain', 'Points','BlogScore'],
              "removeOdds.csv")

    if remover == 3 or remover == 0:
        predictor(columns, ['y', 'Player', 'BPS', 'Round', 'isCaptain', 'Points', 'DefenseOdds', 'OffenceOdds'],
              "removeBlog.csv")
    '''
    if remover == 4 or remover == 0:
        predictor(columns,
                  ['y', 'Player', 'BPS', 'Round', 'isCaptain', 'Points','BlogScore', 'DefenseOdds', 'OffenceOdds'],
              "removeAll.csv")


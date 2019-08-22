import sys
import pandas as pd
import Statistics.Historical.GradientBoosting as GB


def convertToCSV(file_name, df):
    df.to_csv(file_name, encoding='utf-8')


def predict(gw, model):

    toRemove = ['y', 'Player', 'BPS', 'Round', 'isCaptain', 'Points', 'DefenseOdds', 'OffenceOdds', 'BlogScore']
    result = GB.main(toRemove, gw, model)
    names = result[2]

    return result



def predictAll(columns, toRemove, csvName, model):
    df = pd.DataFrame(columns=columns, index=[1])

    for currentGW in range(2, 39):

        result = GB.main(toRemove, currentGW, model)
        print("Average Points = "+str(result[0]))
        print("Total Points = "+str(result[1]))

        for i in range(0, len(result[1])):
            df.at[i+1, "GW_"+str(currentGW)] = result[1][i]

    convertToCSV(csvName, df)

'''
REMOVER VALUES
0 - compare all datasets
1 - remove no values
2 - remove odds
3 - remove blogs
4 - remove everything
5 - GBM vs RF
'''
if __name__ == '__main__':

    '''
    toRemove = ['y', 'Player', 'BPS', 'Round', 'isCaptain', 'Points']
    columns = []
    for i in range(2, 39):
        columns.append("GW_"+str(i))

    predictAll(columns, toRemove, 'gbm.csv', "gbm")
    '''
    import time

    st = time.time()

    predict(3, "gbm")

    print("----%.2f----" % (time.time() - st))

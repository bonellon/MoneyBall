import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier, RandomForestRegressor
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve
from sklearn.metrics import auc

from Statistics.Historical import Player

pd.options.mode.chained_assignment = None  # default='warn'
CURRENT_GAMEWEEK = 3

K_SPLITS = 10

LEARNING_RATE = 0.25
N_ESTIMATORS = 600
MAX_DEPTH = 5
MIN_SAMPLES_LEAFS = 0.02
MAX_FEATURES = 2
SUBSAMPLE = 0.8

CURRENT_PATH = os.path.dirname(__file__)

#0.25
learning_rates = [0.5, 0.25, 0.105]

#600
n_estimators = [500, 600, 750]

#5
max_depths = np.linspace(3, 10, 3, endpoint=True)

min_sample_splits = [0.01, 0.025, 0.05]

#0.02
min_samples_leafs = np.linspace(0.01, 0.05, 3, endpoint=True)

#2
max_features = [2,4,6]

#0.8
subsample = np.linspace(0.5, 1, 3, endpoint=True)

train_results = []
test_results = []

'''
meanValues = ds.groupby(['isCaptain']).mean()
print(meanValues)


GRAPH

correlations = ds.corr()
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(correlations, vmin=-1, vmax=1)
fig.colorbar(cax)
names = ['']+list(ds)
ax.set_xticklabels(names)
ax.set_yticklabels(names)
plt.show()
correlations
'''


def splitTable(df):

    keeperDS = df.drop(df[df.elementID != 1].index)
    defenderDS = df.drop(df[df.elementID != 2].index)
    midfielderDS = df.drop(df[df.elementID != 3].index)
    forwardDS = df.drop(df[df.elementID != 4].index)

    return keeperDS, defenderDS, midfielderDS, forwardDS

#Scales the following columns:
#minutes, ICT_index, Threat, Influence, Transfers_Balance, Value, BPS, DefenseOdds, OffenceOdds
def featureScaling(df):
    from sklearn.preprocessing import MinMaxScaler

    scale = MinMaxScaler()
    df[['minutes', 'ICT_index', 'Threat', 'Influence','Transfers_Balance', 'Value', 'BPS','DefenseOdds', 'OffenceOdds']]\
        = scale.fit_transform(df[['minutes', 'ICT_index', 'Threat', 'Influence',
                                  'Transfers_Balance', 'Value', 'BPS','DefenseOdds', 'OffenceOdds']].values)

    return df

def removeCurrentAndFuture(ds, currentGW):
    ds = ds.drop(ds[ds.Round >= currentGW].index)
    return ds


def getTestTrain(ds, y, toRemove, currentGW):

    ds['y'] = y

    X_train = removeCurrentAndFuture(ds, currentGW)
    X_test = ds.drop(ds[ds.Round != currentGW].index)

    y_train = X_train['y']
    y_test = X_test['y']

    X_train.drop(toRemove, axis=1, inplace=True)
    X_test.drop(toRemove, axis=1, inplace=True)

    return X_train, X_test, y_train, y_test


#Creates X and Y tables - does not split into train/test
#Adds all multiplication columns
def generateTable(ds):
    y = ds.isCaptain
    #y = ds.Points

    GB_table = ds
    GB_table.head()

    points_prev_2prev = GB_table['Points_2PrevWeek'] * GB_table['Points_PrevWeek']
    average_points = (GB_table['Points_2PrevWeek'] + GB_table['Points_PrevWeek']) / 2

    prev_points_fdr = GB_table['Points_PrevWeek'] * GB_table['Opponent_FDR_PrevWeek']
    prev_points_home = GB_table['Points_PrevWeek'] * GB_table['isHome_PrevWeek']

    prev2_points_fdr = GB_table['Points_2PrevWeek'] * GB_table['Opponent_FDR_2PrevWeek']
    prev2_points_home = GB_table['Points_2PrevWeek'] * GB_table['isHome_2PrevWeek']

    GB_table = GB_table.assign(points_prev_2prev=points_prev_2prev, average_points=average_points,
                               prev_points_fdr=prev_points_fdr,
                               prev_points_home=prev_points_home, prev2_points_fdr=prev2_points_fdr,
                               prev2_points_home=prev2_points_home)

    return GB_table, y

def prediction(ds, toRemove, currentGW, baseline):

    GB_table, y = generateTable(ds)

    X_train, X_test, y_train, y_test = getTestTrain(GB_table, y, toRemove, currentGW)

    baseline.fit(X_train, y_train)

    '''
    predictors = list(X_train)
    feat_imp = pd.Series(baseline.feature_importances_, predictors).sort_values(ascending=False)
    feat_imp.plot(kind='bar', title='Importance of Features')
    plt.ylabel('Feature Importance Score')
    plt.show()
    '''
#    print('Accuracy of the GBM on test set: {:.3f}'.format(baseline.score(X_test, y_test)))


    pred = baseline.predict(X_train)

    '''
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_train, pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    train_results.append(roc_auc)
    '''
    pred = baseline.predict(X_test)

    ''' 
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    test_results.append(roc_auc)
    '''
    print(classification_report(y_test, pred.round()))

    pred_original_data = ds.loc[X_test.index]
    pred_original_data['prediction'] = pred
    #pred_original_data.drop(pred_original_data[pred_original_data.prediction < 1].index, inplace=True)

    #pred_original_data.drop(pred_original_data[pred_original_data.prediction <= 6].index, inplace=True)

    return pred_original_data

def writeCleanedCSV(csv):
    csv.to_csv("predictorCleaned.csv")

def getBlogScores(players):
    blogs = (pd.read_csv(CURRENT_PATH+'//..//..//Blogs//playersResult.csv', encoding="ISO-8859-1"))

    players["BlogScore"] = pd.Series(0.00, index=players.index)
    #print("Adding BlogScores...")

    for index,row in blogs.iterrows():
        #print()
        #print(row['cleanName'], end = ' ')

        name = players.drop(players[players.PlayerID != row['ID']].index)

        for index2, row2 in name.iterrows():

            if row2['PlayerID'] == row['ID']:
                try:
                    currentRound = row2['Round']
                    #print(currentRound, end= ' ')
                    roundScore = row['score_'+str(currentRound)]

                    players.at[index2, 'BlogScore'] = roundScore
                except:
                    pass
    return players


def main(toRemove, currentGW, baseline):
    baseline = learningModel(baseline)
    print("Generating predictions...\nGameweek: "+str(currentGW))
    print("Removing Columns: "+str(toRemove))

    ds=(pd.read_csv(CURRENT_PATH+'/Predictor.csv', encoding="ISO-8859-1"))
    ds.fillna(ds.mean(), inplace=True)

    ds = getBlogScores(ds)

    #ds = featureScaling(ds)
    writeCleanedCSV(ds)

    keeperDS, defenderDS, midfielderDS, forwardDS =splitTable(ds)

    names = []
    points = []

    allPoints = []
    print()
    print("Iteration: ", end = ' ')
    for i in range(0,1):
        print(i, end = ' ')
        currentPoints = 0
        current = prediction(keeperDS, toRemove, currentGW, baseline)
        current.sort_values("prediction", ascending=False, inplace=True)
        current = current.head(1)

        temp = []
        for i in range(0, len(current['Player'].tolist())):
            temp.append(Player.Player(current['Player'].tolist()[i], current['Points'].tolist()[i]).__dict__)

        names.append(temp)
        points.append(current['Points'].tolist())

        for point in current['Points']:
            currentPoints = currentPoints + point

        current = prediction(defenderDS, toRemove, currentGW, baseline)
        current.sort_values("prediction", ascending=False, inplace=True)
        current = current.head(4)

        temp = []
        for i in range(0, len(current['Player'].tolist())):
            temp.append(Player.Player(current['Player'].tolist()[i], current['Points'].tolist()[i]).__dict__)

        names.append(temp)
        points.append(current['Points'].tolist())

        for point in current['Points']:
            currentPoints = currentPoints + point

        current = prediction(midfielderDS, toRemove, currentGW, baseline)
        current.sort_values("prediction", ascending=False, inplace=True)
        current = current.head(5)

        temp = []
        for i in range(0, len(current['Player'].tolist())):
            temp.append(Player.Player(current['Player'].tolist()[i], current['Points'].tolist()[i]).__dict__)

        names.append(temp)
        points.append(current['Points'].tolist())

        for point in current['Points']:
            currentPoints = currentPoints + point

        current = prediction(forwardDS, toRemove, currentGW, baseline)
        current.sort_values("prediction", ascending=False, inplace=True)
        current = current.head(1)

        temp = []
        for i in range(0, len(current['Player'].tolist())):
            temp.append(Player.Player(current['Player'].tolist()[i], current['Points'].tolist()[i]).__dict__)

        names.append(temp)
        points.append(current['Points'].tolist())

        for point in current['Points']:
            currentPoints = currentPoints + point

        allPoints.append(currentPoints)

    #print("Finished!")
    totalPoints = 0
    totalPlayers = 0
    for i in range(0, len(names)):
        length = int(len(names[i])/2)
        for j in range(0, length-1):
            totalPoints = totalPoints + int(points[i][j])
            totalPlayers = totalPlayers + 1
            print(names[i][j])

    print("Total Points: "+str(allPoints))
    print("Average Player Points: "+str(allPoints[0]/totalPlayers))
    '''
    from matplotlib.legend_handler import HandlerLine2D
    
    line1, = plt.plot(learning_rates, train_results, 'b', label='Train AUC')
    line2, = plt.plot(learning_rates, test_results, 'r', label='Test AUC')
    plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
    plt.ylabel('AUC score')
    plt.xlabel('learning rate')
    plt.show()
    '''

    return totalPoints/totalPlayers, allPoints, names

def learningModel(choice):
    if choice == "gbm":
        return GradientBoostingClassifier(learning_rate=LEARNING_RATE, n_estimators=N_ESTIMATORS, max_depth=MAX_DEPTH,
                                          min_samples_split=MIN_SAMPLES_LEAFS, min_samples_leaf=MIN_SAMPLES_LEAFS,
                                          max_features=MAX_FEATURES, subsample=SUBSAMPLE, verbose=False)
    if choice == "svm":
        return SVC(kernel='linear')

    else:
        return RandomForestRegressor(n_estimators=N_ESTIMATORS, random_state=0)


if __name__ == '__main__':
    toRemove = ['y', 'Player', 'BPS', 'Round', 'isCaptain', 'Points'] #,'BlogScore', 'DefenseOdds', 'OffenceOdds']

    baseline = "rf"



    main(toRemove, CURRENT_GAMEWEEK, baseline)


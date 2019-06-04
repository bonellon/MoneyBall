import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve
from sklearn.metrics import auc

pd.options.mode.chained_assignment = None  # default='warn'
CURRENT_GAMEWEEK = 38

K_SPLITS = 10

LEARNING_RATE = 0.25
N_ESTIMATORS = 600
MAX_DEPTH = 5
MIN_SAMPLES_LEAFS = 0.02
MAX_FEATURES = 2
SUBSAMPLE = 0.8


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

def removeCurrentAndFuture(ds):
    ds = ds.drop(ds[ds.Round >= CURRENT_GAMEWEEK].index)
    return ds


def getTestTrain(ds, y):

    ds['y'] = y

    X_train = removeCurrentAndFuture(ds)
    X_test = ds.drop(ds[ds.Round != CURRENT_GAMEWEEK].index)

    y_train = X_train['y']
    y_test = X_test['y']

    X_train.drop(['y', 'Player', 'Round', 'isCaptain', 'Points'], axis=1, inplace=True)
    X_test.drop(['y', 'Player', 'Round', 'isCaptain', 'Points'], axis=1, inplace=True)

    return X_train, X_test, y_train, y_test


def predictionRandom(ds):

    #remove current & all next gameweeks
    ds = removeCurrentAndFuture(ds)
    X, y = generateTable(ds)

    from sklearn.model_selection import RepeatedKFold

#what is n_repeats???
    kf = RepeatedKFold(n_splits=5, n_repeats=1, random_state=None)

    for train_index, test_index in kf.split(X,y):
        print("Train:", train_index, "Validation:", test_index)

        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        X_train.drop(['Player', 'Round', 'isCaptain', 'Points'], axis=1, inplace=True)
        X_test.drop(['Player', 'Round', 'isCaptain', 'Points'], axis=1, inplace=True)

        getPredictionResults(X_train, y_train, X_test, y_test)

#plot ROC graphs from test and training set
#print classification report
#print accuracy
def getPredictionResults(X_train, y_train, X_test, y_test):
    baseline = GradientBoostingClassifier(learning_rate=LEARNING_RATE, n_estimators=N_ESTIMATORS, max_depth=MAX_DEPTH,
                                          min_samples_split=MIN_SAMPLES_LEAFS, min_samples_leaf=MIN_SAMPLES_LEAFS,
                                          max_features=MAX_FEATURES, subsample=SUBSAMPLE, verbose=False)

    baseline.fit(X_train, y_train)
    pred = baseline.predict(X_train)

    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_train, pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    train_results.append(roc_auc)

    pred = baseline.predict(X_test)

    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    test_results.append(roc_auc)

    print(classification_report(y_test, pred))

    pred_original_data = ds.iloc[X_test.index]
    pred_original_data['prediction'] = pred
    # pred_original_data.drop(pred_original_data[pred_original_data.prediction < 1].index, inplace=True)

    pred_original_data.drop(pred_original_data[pred_original_data.isCaptain < 1].index, inplace=True)

    print('Accuracy of GBM on test set: {:.3f}'.format(baseline.score(X_test, y_test)))


#Creates X and Y tables - does not split into train/test
#Adds all multiplication columns
def generateTable(ds):
    y = ds.isCaptain
    # y = ds.Points

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

def prediction(ds,i):

    GB_table, y = generateTable(ds)

    X_train, X_test, y_train, y_test = getTestTrain(GB_table, y)
    #X_train, X_test, y_train, y_test = train_test_split(GB_table, y, test_size=getTestSize(ds), shuffle=False)

    baseline = GradientBoostingClassifier(learning_rate=learning_rates[i], n_estimators=n_estimators[i], max_depth=max_depths[i],
                                          min_samples_split=min_sample_splits[i], min_samples_leaf=min_samples_leafs[i],
                                          max_features=max_features[i], subsample=subsample[i], verbose=False)

    baseline.fit(X_train, y_train)

    predictors = list(X_train)
    feat_imp = pd.Series(baseline.feature_importances_, predictors).sort_values(ascending=False)
    feat_imp.plot(kind='bar', title='Importance of Features')
    plt.ylabel('Feature Importance Score')
    plt.show()
#    print('Accuracy of the GBM on test set: {:.3f}'.format(baseline.score(X_test, y_test)))


    pred = baseline.predict(X_train)

    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_train, pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    train_results.append(roc_auc)

    pred = baseline.predict(X_test)

    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    test_results.append(roc_auc)

    print(classification_report(y_test, pred))

    pred_original_data = ds.loc[X_test.index]
    pred_original_data['prediction'] = pred
    #pred_original_data.drop(pred_original_data[pred_original_data.prediction < 1].index, inplace=True)

    pred_original_data.drop(pred_original_data[pred_original_data.prediction < 1].index, inplace=True)

    return pred_original_data, train_results, test_results


ds=(pd.read_csv('Predictor.csv', encoding="ISO-8859-1"))
ds.fillna(ds.mean(), inplace=True)
ds = featureScaling(ds)

keeperDS, defenderDS, midfielderDS, forwardDS =splitTable(ds)

names = []
points = []
train_results = []
test_results = []


for i in range(0,1):
    current = prediction(keeperDS, i)
    names.append(current[0]['Player'].tolist())
    points.append(current[0]['Points'].tolist())
    train_results.append(current[1])
    test_results.append(current[2])

    current = prediction(defenderDS, i)
    names.append(current[0]['Player'].tolist())
    points.append(current[0]['Points'].tolist())
    train_results.append(current[1])
    test_results.append(current[2])

    current = prediction(midfielderDS, i)
    names.append(current[0]['Player'].tolist())
    points.append(current[0]['Points'].tolist())
    train_results.append(current[1])
    test_results.append(current[2])

    current = prediction(forwardDS, i)
    names.append(current[0]['Player'].tolist())
    points.append(current[0]['Points'].tolist())
    train_results.append(current[1])
    test_results.append(current[2])

print("Finished!")
for i in range(0, len(names)):
    print(names[i])
    #for j in range(0, len(names[i])-1):
     #   print(names[i][j] + "  "+ str(points[i][j]))
'''
from matplotlib.legend_handler import HandlerLine2D

line1, = plt.plot(learning_rates, train_results, 'b', label='Train AUC')
line2, = plt.plot(learning_rates, test_results, 'r', label='Test AUC')
plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
plt.ylabel('AUC score')
plt.xlabel('learning rate')
plt.show()
'''


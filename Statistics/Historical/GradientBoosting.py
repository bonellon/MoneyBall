import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve
from sklearn.metrics import auc

pd.options.mode.chained_assignment = None  # default='warn'
CURRENT_GAMEWEEK = 36

ds=(pd.read_csv('Predictor.csv', encoding="ISO-8859-1"))

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

def getTestTrain(ds, y):

    ds['y'] = y

    X_train = ds.drop(ds[ds.Round >= CURRENT_GAMEWEEK].index)
    X_test = ds.drop(ds[ds.Round != CURRENT_GAMEWEEK].index)

    y_train = X_train['y']
    y_test = X_test['y']

    X_train.drop(['y', 'Player', 'Round', 'isCaptain', 'Points'], axis=1, inplace=True)
    X_test.drop(['y', 'Player', 'Round', 'isCaptain', 'Points'], axis=1, inplace=True)

    return X_train, X_test, y_train, y_test

def prediction(ds, learning_rate, n_estimators, max_depth, min_samples_split, min_samples_leaf, max_features, subsample):
    y = ds.isCaptain
    #y = ds.Points

    train_results = []
    test_results = []

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

    X_train, X_test, y_train, y_test = getTestTrain(GB_table, y)
    #X_train, X_test, y_train, y_test = train_test_split(GB_table, y, test_size=getTestSize(ds), shuffle=False)

    baseline = GradientBoostingClassifier(learning_rate=learning_rate, n_estimators=n_estimators, max_depth=max_depth,
                                          min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf,
                                          max_features=max_features, subsample=subsample, verbose=10)
    baseline.fit(X_train, y_train)
    #predictors = list(X_train)
    #feat_imp = pd.Series(baseline.feature_importances_, predictors).sort_values(ascending=False)
    #feat_imp.plot(kind='bar', title='Importance of Features')
    #plt.ylabel('Feature Importance Score')
    #plt.show()
    print('Accuracy of GBM on test set: {:.3f}'.format(baseline.score(X_test, y_test)))


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
    pred_original_data.drop(pred_original_data[pred_original_data.prediction < 1].index, inplace=True)

    return pred_original_data, train_results, test_results

names = []
train_results = []
test_results = []

#0.25
learning_rates = [1, 0.75, 0.5, 0.25, 0.1, 0.075, 0.05]

#600
n_estimators = [1, 2, 4, 8, 16, 32, 64, 100, 250, 500, 600, 750, 1000]

#5
max_depths = np.linspace(1, 32, 32, endpoint=True)

#0.02
min_samples_leafs = np.linspace(0.00001, 0.5, 100, endpoint=True)

#2
max_features = [1,2,3,4,5,6,7,8,9,10]

subsample = np.linspace(0.0001, 1, 20, endpoint=True)


currentTest = subsample
for test in currentTest:

    current = prediction(ds, learning_rate=0.25, n_estimators=600, max_depth=5, min_samples_split=2,
           min_samples_leaf=0.02, max_features=2, subsample=0.8)
    names.append(current[0]['Player'].tolist())
    train_results.append(current[1])
    test_results.append(current[2])

print("Finished")
for name in names:
    print(name)

from matplotlib.legend_handler import HandlerLine2D
line1, = plt.plot(currentTest, train_results, 'b', label='Train AUC')
line2, = plt.plot(currentTest, test_results, 'r', label='Test AUC')
plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
plt.ylabel('AUC score')
plt.xlabel('learning rate')
plt.show()
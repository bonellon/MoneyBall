import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report

pd.options.mode.chained_assignment = None  # default='warn'
CURRENT_GAMEWEEK = 34

ds=pd.read_csv('Predictor.csv', encoding="ISO-8859-1")
#ds.head()

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

def prediction(ds, learning_rate, n_estimators, max_depth, min_samples_split, min_samples_leaf, max_features, subsample, random_state):
    y = ds.isCaptain
    GB_table = ds.drop(['Player', 'Round', 'isCaptain', 'Points'], axis=1)
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

    X_train, X_test, y_train, y_test = train_test_split(GB_table, y, test_size=0.2)

    baseline = GradientBoostingClassifier(learning_rate=learning_rate, n_estimators=n_estimators, max_depth=max_depth,
                                          min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf,
                                          max_features=max_features, subsample=subsample, random_state=random_state)
    baseline.fit(X_train, y_train)
    predictors = list(X_train)
    feat_imp = pd.Series(baseline.feature_importances_, predictors).sort_values(ascending=False)
    feat_imp.plot(kind='bar', title='Importance of Features')
    plt.ylabel('Feature Importance Score')
    # plt.show()
    #print('Accuracy of GBM on test set: {:.3f}'.format(baseline.score(X_test, y_test)))
    pred = baseline.predict(X_test)
    print(classification_report(y_test, pred))

    pred_original_data = ds.iloc[X_test.index]
    pred_original_data['prediction'] = pred
    pred_original_data.drop(pred_original_data[pred_original_data.prediction < 1].index, inplace=True)

    return len(pred_original_data.index)

count = 0
for i in range(0,1):
    print(i)
    count += prediction(ds, learning_rate=0.01, n_estimators=550, max_depth=4, min_samples_split=40,
           min_samples_leaf=7, max_features=6, subsample=0.95, random_state=10)
print("Average Count = "+str(count/50))
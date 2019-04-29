import pandas as pd
import sys
import numpy as np
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as sk
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
from sklearn.grid_search import GridSearchCV

ds=pd.read_csv('Predictor.csv', encoding="ISO-8859-1")
#ds.head()

ds.head()
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


y = ds.isCaptain
GB_table = ds.drop(['Player', 'Round', 'isCaptain', 'Points', 'Opponent'], axis=1)
GB_table.head()

points_prev_2prev = GB_table['Points_2PrevWeek'] * GB_table['Points_PrevWeek']
average_points = (GB_table['Points_2PrevWeek'] + GB_table['Points_PrevWeek'])/2

prev_points_fdr = GB_table['Points_PrevWeek'] * GB_table['Opponent_FDR_PrevWeek']
prev_points_home = GB_table['Points_PrevWeek'] * GB_table['isHome_PrevWeek']

prev2_points_fdr = GB_table['Points_2PrevWeek'] * GB_table['Opponent_FDR_2PrevWeek']
prev2_points_home = GB_table['Points_2PrevWeek'] * GB_table['isHome_2PrevWeek']

GB_table = GB_table.assign(points_prev_2prev=points_prev_2prev, average_points = average_points, prev_points_fdr = prev_points_fdr,
                           prev_points_home = prev_points_home, prev2_points_fdr = prev2_points_fdr, prev2_points_home = prev2_points_home)

X_train, X_test, y_train, y_test = train_test_split(GB_table, y, test_size=0.2)

baseline = GradientBoostingClassifier(learning_rate=0.1, n_estimators=100,max_depth=3, min_samples_split=2, min_samples_leaf=1, subsample=1,max_features='sqrt', random_state=10)
baseline.fit(X_train,y_train)
predictors=list(X_train)
feat_imp = pd.Series(baseline.feature_importances_, predictors).sort_values(ascending=False)
feat_imp.plot(kind='bar', title='Importance of Features')
plt.ylabel('Feature Importance Score')
#plt.show()
print('Accuracy of GBM on test set: {:.3f}'.format(baseline.score(X_test, y_test)))
pred=baseline.predict(X_test)
print(classification_report(y_test, pred))

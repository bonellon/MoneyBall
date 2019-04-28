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

ds=pd.read_csv('Predictor.csv', encoding="ISO-8859-1")
#ds.head()

ds.head()
meanValues = ds.groupby(['isCaptain']).mean()
print(meanValues)

'''
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
testTable = ds.drop(['isCaptain', 'Points_NextWeek', 'Points'], axis=1)
testTable.head()


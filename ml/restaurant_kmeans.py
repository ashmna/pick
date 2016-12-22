import pandas
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

data = pandas.read_csv('../resources/menu/timestamp_Wday.csv')

data['InRestaurant'] = data['TimePick'] - data['TimeArrive']

aData = data[data['InRestaurant'] > 0]

# bData = aData
bData = aData[aData['InRestaurant'] <= 3600]

newData = pandas.DataFrame()

def r(val):
    return np.random.randint(1, 100)

newData['random'] = bData.InRestaurant.map(r)

newData['InRestaurant'] = bData.InRestaurant

X = newData.as_matrix()

y_pred = KMeans(n_clusters=3).fit_predict(X)


plt.figure(1)
plt.clf()

plt.scatter(X[:, 0], X[:, 1], c=y_pred)
plt.title("Unevenly Sized Blobs")

plt.show()

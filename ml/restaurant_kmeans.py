import matplotlib.pyplot as plt
import numpy as np
import pandas
from sklearn.cluster import KMeans

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


kMeans = KMeans(n_clusters=3)
kMeans.fit(X)

y_pred = kMeans.predict(X)



# from sklearn.externals import joblib
# joblib.dump(kMeans, 'model/3-means.pkl')

plt.figure(1)
plt.clf()

plt.scatter(X[:, 0], X[:, 1], c=y_pred)
plt.title("Time Spent In Restaurant")

plt.show()

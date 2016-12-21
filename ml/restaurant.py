import pandas
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth

data = pandas.read_csv('../resources/menu/timestamp_Wday.csv')

data['InRestaurant'] = data['TimePick'] - data['TimeArrive']

aData = data[data['InRestaurant'] > 0]

bData = aData[aData['InRestaurant'] <= 3600]

newData = pandas.DataFrame()

def r(val):
    return np.random.randint(1, 100)

newData['random'] = bData.InRestaurant.map(r)

newData['InRestaurant'] = bData.InRestaurant

X = newData.as_matrix()

bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=10000)

ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(X)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

print("number of estimated clusters : %d" % n_clusters_)

import matplotlib.pyplot as plt
from itertools import cycle

plt.figure(1)
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    my_members = labels == k
    cluster_center = cluster_centers[k]
    plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)
plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()

# head = data.head()


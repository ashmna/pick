import matplotlib.pyplot as plt
import numpy as np
import pandas
from sklearn.cluster import KMeans
#
# data = pandas.read_csv('../resources/menu/timestamp_Wday.csv')
# # data.set_index('ID')
# order_items = pandas.read_csv('../resources/menu/menu.am/OrderItems.csv')
# # data.set_index('OrderNumber')
#
# data = pandas.merge(data, order_items, left_on='ID', right_on='OrderNumber')
# data['cookingTime'] = data['TimePick'] - data['TimePlace']
# data['time'] = data.TimePlace - data.TransDate
# # data['Restaurant_x'].value_counts()
# # 284
# # 597
# # 353
# # 386
# # 51
#
# data_284 = data[data['Restaurant_x'] == 284]
# data_51 = data[data['Restaurant_x'] == 51]
# data_51 = data_51[data['time'].notnull()]
# data_51 = data_51[data['cookingTime'].notnull()]
#
#
# # print data_284['ItemNumber'].value_counts()
# # 46.0     3708
# # 126.0    1918
# # 2.0      1354
# # 14.0     1329
# # 58.0      774
#
# # print data_51['ItemNumber'].value_counts()
# # 244.0    507
# # 72.0     349
# # 220.0    348
# # 71.0     287
# # 194.0    252
# data_51_244 = data_51[data_51['ItemNumber'] == 244]
# data_51_72 = data_51[data_51['ItemNumber'] == 72]
# data_51_220 = data_51[data_51['ItemNumber'] == 220]
# data_51_71 = data_51[data_51['ItemNumber'] == 71]
# data_51_194 = data_51[data_51['ItemNumber'] == 194]
#
# from sklearn import neighbors
#
# data_51_220.to_csv('./data_51_220.csv')
data_51_220 = pandas.read_csv('./data_51_220.csv')

n_neighbors = 5

T = np.linspace(0, 5, 500)[:, np.newaxis]
XDataFrame = pandas.DataFrame()
XDataFrame['time'] = data_51_220['time'].as_matrix()
X = XDataFrame.as_matrix()

y = data_51_220['cookingTime'].as_matrix()


#
from sklearn.neighbors import KNeighborsRegressor
knn = KNeighborsRegressor(n_neighbors=len(X)/6, weights='uniform')
knn.fit(X, y)



bx = []
for item in range(0, 24 * 60 * 60):
    bx.append([item])
by = knn.predict(bx)

print len(bx)
print len(by)

fig = plt.figure(1)
plt.clf()

plt.scatter(X, y, c='k', label='data')
plt.plot(bx, by, '-g')

plt.show()

# for i, weights in enumerate(['uniform', 'distance']):
#     knn = neighbors.KNeighborsRegressor(n_neighbors, weights=weights)
#     y_ = knn.fit(X, y).predict(T)
#
#     plt.subplot(2, 1, i + 1)
#     plt.scatter(X, y, c='k', label='data')
#     plt.plot(T, y_, c='g', label='prediction')
#     plt.axis('tight')
#     plt.legend()
#     plt.title("KNeighborsRegressor (k = %i, weights = '%s')" % (n_neighbors, weights))
#
# plt.show()


# print data.head()
#
# data['InRestaurant'] = data['TimePick'] - data['TimeArrive']
#
# aData = data[data['InRestaurant'] > 0]
#
# # bData = aData
# bData = aData[aData['InRestaurant'] <= 3600]
#
# newData = pandas.DataFrame()
#
# def r(val):
#     return np.random.randint(1, 100)
#
# newData['random'] = bData.InRestaurant.map(r)
#
# newData['InRestaurant'] = bData.InRestaurant
#
# X = newData.as_matrix()
#
#
# kMeans = KMeans(n_clusters=3)
# kMeans.fit(X)
#
# y_pred = kMeans.predict(X)
#
#

# from sklearn.externals import joblib
# joblib.dump(kMeans, 'model/3-means.pkl')

# plt.figure(1)
# plt.clf()
#
# plt.scatter(X[:, 0], X[:, 1], c=y_pred)
# plt.title("Unevenly Sized Blobs")
#
# plt.show()
#
import pandas
from xgboost import XGBRegressor
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold, train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, mean_squared_error
from sklearn import linear_model

rng = np.random.RandomState(31337)


def to_nested_list(arr, rate, week_day):
    tmp_data = []
    for item in arr:
        r = [item, rate / 10.0, 0, 0, 0, 0, 0, 0, 0]
        r[week_day + 2] = 1
        tmp_data.append(r)
    return np.array(tmp_data)


data = pandas.read_csv('../data/courier-merge-data.csv')

data = data[data['distance'] > 1]
data = data[data['time_in_route'] > 4 * 60]
data = data[data['km_h'] < 35]
data = data[data['km_h'] > 5]

# part1 = data[data['time'] < 6*60*60]
# part1['time'] += 24*60*60
#
# part2 = data[data['time'] > 6*60*60]
# part2['time'] -= 24*60*60
#
#
# data = pandas.concat([data, part1, part2])


X_list = []
for index, row in data.iterrows():
    courier_rate = 0.9
    if row['courier'] == 1085:
        courier_rate = 1.0
    r = [row['time'], courier_rate / 10.0, 0, 0, 0, 0, 0, 0, 0]
    r[row['week_day'] + 2] = 1
    X_list.append(r)
X = np.array(X_list)
# for item in data:
#     print item['time']
#     print item

# X = to_nested_list(data['time'])
y = np.array(data['km_h'].as_matrix())

#
# kf = KFold(n_splits=2, shuffle=True, random_state=rng)
# for train_index, test_index in kf.split(X):
#     xgb_model = XGBRegressor().fit(X[train_index], y[train_index])
#     predictions = xgb_model.predict(X[test_index])
#     actuals = y[test_index]
#     print(mean_squared_error(actuals, predictions))



# reg = linear_model.RidgeCV()
# reg.fit(X, y)
xgb_model = XGBRegressor(
    max_depth=7,
    n_estimators=250
)
xgb_model.fit(X, y)
#
#
#
#
#
# tx = np.arange(0.0, 24 * 60 * 60, 10 * 60)
tx1_0 = to_nested_list(range(0, 24 * 60 * 60, 10 * 60), 0.7, 0)
tx1_1 = to_nested_list(range(0, 24 * 60 * 60, 10 * 60), 0.7, 1)
tx1_2 = to_nested_list(range(0, 24 * 60 * 60, 10 * 60), 0.7, 2)
tx1_3 = to_nested_list(range(0, 24 * 60 * 60, 10 * 60), 0.7, 3)
tx1_4 = to_nested_list(range(0, 24 * 60 * 60, 10 * 60), 0.7, 4)
tx1_5 = to_nested_list(range(0, 24 * 60 * 60, 10 * 60), 0.7, 5)
tx1_6 = to_nested_list(range(0, 24 * 60 * 60, 10 * 60), 0.7, 6)
tx2_0 = to_nested_list(range(0, 24 * 60 * 60, 10 * 60), 1.0, 0)
tx2_1 = to_nested_list(range(0, 24 * 60 * 60, 10 * 60), 1.0, 1)
tx2_2 = to_nested_list(range(0, 24 * 60 * 60, 10 * 60), 1.0, 2)
tx2_3 = to_nested_list(range(0, 24 * 60 * 60, 10 * 60), 1.0, 3)
tx2_4 = to_nested_list(range(0, 24 * 60 * 60, 10 * 60), 1.0, 4)
tx2_5 = to_nested_list(range(0, 24 * 60 * 60, 10 * 60), 1.0, 5)
tx2_6 = to_nested_list(range(0, 24 * 60 * 60, 10 * 60), 1.0, 6)
#
# print tx
#
# # print to_nested_list(tx)
#
ty1_0= xgb_model.predict(tx1_0)
ty1_1= xgb_model.predict(tx1_1)
ty1_2= xgb_model.predict(tx1_2)
ty1_3= xgb_model.predict(tx1_3)
ty1_4= xgb_model.predict(tx1_4)
ty1_5= xgb_model.predict(tx1_5)
ty1_6= xgb_model.predict(tx1_6)
ty2_0 = xgb_model.predict(tx2_0)
ty2_1 = xgb_model.predict(tx2_1)
ty2_2 = xgb_model.predict(tx2_2)
ty2_3 = xgb_model.predict(tx2_3)
ty2_4 = xgb_model.predict(tx2_4)
ty2_5 = xgb_model.predict(tx2_5)
ty2_6 = xgb_model.predict(tx2_6)


plt.figure(1)
plt.plot(X, y, 'bo')
plt.plot(tx1_0, ty1_0, 'k')
plt.plot(tx1_1, ty1_1, 'k')
plt.plot(tx1_2, ty1_2, 'k')
plt.plot(tx1_3, ty1_3, 'k')
plt.plot(tx1_4, ty1_4, 'k')
plt.plot(tx1_5, ty1_5, 'k')
plt.plot(tx1_6, ty1_6, 'k')
plt.plot(tx2_0, ty2_0, 'r')
plt.plot(tx2_1, ty2_1, 'r')
plt.plot(tx2_2, ty2_2, 'r')
plt.plot(tx2_3, ty2_3, 'r')
plt.plot(tx2_4, ty2_4, 'r')
plt.plot(tx2_5, ty2_5, 'r')
plt.plot(tx2_6, ty2_6, 'r')


plt.show()











# xgb.fit()









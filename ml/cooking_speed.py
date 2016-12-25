import pandas
import numpy
from sklearn.externals import joblib
from sklearn.isotonic import IsotonicRegression
import matplotlib.pyplot as plt

kMeans = joblib.load('model/3-means.pkl')

restaurant = 159
driver = 1111

all_data = pandas.read_csv('../resources/menu/timestamp_Wday.csv')

data = all_data[all_data.Restaurant == restaurant]

data['InRestaurant'] = data['TimePick'] - data['TimeArrive']
data = data[data['InRestaurant'] > 0]
data = data[data['InRestaurant'] <= 3600]

newData = pandas.DataFrame()
def r(val):
    return numpy.random.randint(1, 100)

newData['random'] = data.InRestaurant.map(r)
newData['InRestaurant'] = data.InRestaurant


data['classifier'] = kMeans.predict(newData.as_matrix())
data = data[data.classifier == 1]

data['cookingTime'] = data.TimePick - data.TimePlace
data['time'] = data.TimePlace - data.TransDate
# data = data[data['cookingTime'] < 27*60]
data = data[data['cookingTime'] > 0]

data_w_0 = data[data.wDay == 0]
data_w_1 = data[data.wDay == 1]
data_w_2 = data[data.wDay == 2]
data_w_3 = data[data.wDay == 3]
data_w_4 = data[data.wDay == 4]
data_w_5 = data[data.wDay == 5]
data_w_6 = data[data.wDay == 6]

def show_data(w_data):
    x = w_data['time'].as_matrix()
    y = w_data['cookingTime'].as_matrix()
    ir = IsotonicRegression()
    ir.fit(x, y)
    bx = range(0, 24 * 60 * 60)
    by = ir.transform(bx)
    plt.plot(x, y, '.')
    plt.plot(bx, by, '-')

fig = plt.figure()
show_data(data_w_0)
show_data(data_w_1)
show_data(data_w_2)
show_data(data_w_3)
show_data(data_w_4)
show_data(data_w_5)
show_data(data_w_6)
# show_data(data)
plt.show()



# x = data_w_4['time'].as_matrix()
# y = data_w_4['cookingTime'].as_matrix()
# ir_w_4 = IsotonicRegression()
# ir_w_4.fit(x, y)
# y_ = ir_w_4.transform(x)
#
# b4x = range(0, 24*60*60)
# b4y = ir_w_4.transform(bx)

# fig = plt.figure()
# plt.plot(x, y, 'r.')
# plt.plot(x, y_, 'g.')
# plt.plot(bx, by, 'b-')
# plt.legend(('Data', 'Isotonic Fit'), loc='lower right')
# plt.title('Isotonic regression')
# plt.show()


# data = data[all_data.Restaurant == restaurant]
#
# TimePlace

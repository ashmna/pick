import matplotlib.pyplot as plt
import pandas
from sklearn.isotonic import IsotonicRegression

restaurant = 159
driver = 1111

all_data = pandas.read_csv('../resources/menu/timestamp_Wday.csv')

all_data['InRestaurant'] = all_data['TimePick'] - all_data['TimeArrive']
all_data = all_data[all_data['InRestaurant'] > 0]
all_data = all_data[all_data['InRestaurant'] <= 3600]

all_data['time'] = all_data['TimeArrive'] - all_data['TransDate']
delta = 9.5*60*60
def ss(time):
    if time < delta:
        return time + 24 * 60 * 60 - delta
    return time - delta

all_data['time'] = all_data['time'].map(ss)


def show_data(w_data):
    x = w_data['time'].as_matrix()
    y = w_data['InRestaurant'].as_matrix()

    ir = IsotonicRegression()
    ir.fit(x, y)

    bx = range(0, 24 * 60 * 60)
    by = ir.predict(bx)
    plt.plot(x, y, '.')
    plt.plot(bx, by, '-')



def show_driver(driver):

    data = all_data[all_data.Driver == driver]

    show_data(data)
    # newData = pandas.DataFrame()
    # newData['random'] = data.InRestaurant.map(lambda val: numpy.random.randint(1, 10))
    # newData['InRestaurant'] = data.InRestaurant

# kMeans = KMeans(n_clusters=2)
# data['classifier'] = kMeans.fit_predict(newData.as_matrix())

# data = data[data.classifier == 0]

# data_w_0 = data[data.wDay == 0]
# data_w_1 = data[data.wDay == 1]
# data_w_2 = data[data.wDay == 2]
# data_w_3 = data[data.wDay == 3]
# data_w_4 = data[data.wDay == 4]
# data_w_5 = data[data.wDay == 5]
# data_w_6 = data[data.wDay == 6]



fig = plt.figure()
# show_data(data_w_0)
# show_data(data_w_1)
# show_data(data_w_2)
# show_data(data_w_3)
# show_data(data_w_4)
# show_data(data_w_5)
# show_data(data_w_6)
# show_data(data)

# show_driver(774)
# show_driver(852)
# show_driver(1121)
# show_driver(1056)
# show_driver(1031)
# show_driver(935)
# show_driver(1118)
# show_driver(1084)
# show_driver(870)
# show_driver(381)
show_driver(1111)

plt.show()

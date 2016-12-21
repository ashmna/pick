import pandas

data = pandas.read_csv('../resources/menu/OrderEntry-2.csv')

data['InRestaurant'] = data['TimePick'] - data['TimeArrive']

head = data.head()

r = 5

import os.path

import pandas
from sklearn import neighbors
from sklearn.externals import joblib

from data_result import DataResult, AnyResult


class Restaurant:
    def __init__(self):
        self.restaurants_address = pandas.read_csv('data/restaurants-address.csv')
        self.order_items = pandas.read_csv('data/order-items.csv')

    def get_restaurants(self):
        restaurants_address = self.restaurants_address[self.restaurants_address['city'] == 'Yerevan']
        return DataResult(restaurants_address)

    def get_restaurant_items(self, restaurant_id):
        order_items = self.order_items[self.order_items['Restaurant'] == restaurant_id]
        return DataResult(order_items)

    def get_restaurant_item_cooking_speed(self, restaurant_id, item_number):
        model = self.__load_cooking_speed_model(restaurant_id, item_number)
        x = self.__to_nested_list(range(0, 24 * 60 * 60, 10 * 60))
        y = model.predict(x).tolist()

        for idx, val in enumerate(y):
            time = x[idx][0]
            x[idx][0] = '%02d:%02d' % ((time / 60 / 60) % 24, (time / 60) % 60)
            x[idx].append(val / 60)

        return AnyResult(x)

    def generate_cooking_speed_data(self):
        orders = pandas.read_csv('data/orders.csv')
        data = pandas.merge(orders, self.order_items, left_on='ID', right_on='OrderNumber')

        data['cookingTime'] = data['TimePick'] - data['TimePlace']
        data['time'] = data.TimePlace - data.TransDate
        data = data[data['time'] > 0]
        data = data[data['cookingTime'] > 0]
        data = data[data['time'].notnull()]
        data = data[data['cookingTime'].notnull()]

        result = list()

        restaurants = data.groupby('Restaurant_x')

        for restaurant_id, data_restaurant in restaurants:
            if len(data_restaurant) < 20:
                continue
            items = data_restaurant.groupby('ItemNumber')

            item_data = pandas.DataFrame()
            item_data['cookingTime'] = data_restaurant['cookingTime']
            item_data['time'] = data_restaurant['time']
            path = 'data/cooking-speed/%d-0.csv' % (int(restaurant_id))
            item_data.to_csv(path)

            for item_number, item_data_all in items:
                if len(item_data_all) < 15:
                    continue
                item_data = pandas.DataFrame()
                item_data['cookingTime'] = item_data_all['cookingTime']
                item_data['time'] = item_data_all['time']

                path = 'data/cooking-speed/%d-%d.csv' % (int(restaurant_id), int(item_number))

                item_data.to_csv(path)

                result.append({
                    "restaurantId": restaurant_id,
                    "itemNumber": item_number,
                    "itemCounts": len(item_data),
                    "path": path,
                })

        return AnyResult(result)

    def __load_cooking_speed_model(self, restaurant_id, item_number):
        path = 'model/cooking-speed/knn-%d-%d.pkl' % (int(restaurant_id), int(item_number))
        if os.path.isfile(path):
            return joblib.load(path)
        res = self.__train_cooking_speed_model(path, restaurant_id, item_number)
        if not res and item_number:
            return self.__load_cooking_speed_model(restaurant_id, 0)
        return joblib.load(path)

    def __load_cooking_speed_data(self, restaurant_id, item_number):
        path = 'data/cooking-speed/%d-%d.csv' % (int(restaurant_id), int(item_number))
        if not os.path.isfile(path):
            return None
        return pandas.read_csv(path)

    def __train_cooking_speed_model(self, path, restaurant_id, item_number=0):
        data = self.__load_cooking_speed_data(restaurant_id, item_number)
        if data is None:
            return False
        x = self.__to_nested_list(data['time'])
        y = data['cookingTime'].as_matrix()
        knn = neighbors.KNeighborsRegressor(n_neighbors=len(x) / 6, weights='uniform')
        knn.fit(x, y)
        joblib.dump(knn, path)
        return True

    def __to_nested_list(self, arr):
        data = []
        for item in arr:
            data.append([item])
        return data

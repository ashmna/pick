import os.path
from math import radians, cos, sin, asin, sqrt

import numpy as np
import pandas
from sklearn import neighbors
from sklearn.externals import joblib

from data_result import AnyResult


class Courier:
    def __init__(self):
        self.client_address = pandas.read_csv('data/client-address.csv')
        self.restaurants_address = pandas.read_csv('data/restaurants-address.csv')
        self.orders = pandas.read_csv('data/orders.csv')
        self.data = self.__merge_data()

    def __merge_data(self):
        courier_merge_data_file_path = 'data/courier-merge-data.csv'
        if os.path.isfile(courier_merge_data_file_path):
            return pandas.read_csv(courier_merge_data_file_path)

        self.restaurants_address['lat_restaurant'] = self.restaurants_address['lat']
        self.restaurants_address['lng_restaurant'] = self.restaurants_address['lng']
        self.restaurants_address['city_restaurant'] = self.restaurants_address['city']

        self.client_address['lat_client'] = self.client_address['lat']
        self.client_address['lng_client'] = self.client_address['lng']

        data = pandas.merge(self.orders, self.restaurants_address, left_on='Restaurant', right_on='ID')
        data = pandas.merge(data, self.client_address, left_on='Customer', right_on='ID')

        data = data[data['city_restaurant'] == 'Yerevan']
        data = data[data['lat_client'].notnull()]
        data = data[data['lng_client'].notnull()]
        data = data[data['lat_client'] > 0]
        data = data[data['lng_client'] > 0]

        data = data[data['TimePick'].notnull()]
        data = data[data['TimeComplete'].notnull()]

        courier_merge_data = pandas.DataFrame()
        courier_merge_data['courier'] = data['Driver']
        courier_merge_data['customer'] = data['Customer']
        courier_merge_data['restaurant'] = data['Restaurant']

        courier_merge_data['lat_client'] = data['lat_client']
        courier_merge_data['lng_client'] = data['lng_client']
        courier_merge_data['lat_restaurant'] = data['lat_restaurant']
        courier_merge_data['lng_restaurant'] = data['lng_restaurant']

        courier_merge_data['transaction_date'] = data['TransDate']
        courier_merge_data['week_day'] = data['wDay']
        courier_merge_data['time'] = data['TimePick'] - data['TransDate']
        courier_merge_data['time_pick'] = data['TimePick']
        courier_merge_data['time_complete'] = data['TimeComplete']

        courier_merge_data['address_restaurant'] = data['street']
        courier_merge_data['address_client'] = data['address']

        distances = list()
        for index, row in courier_merge_data.iterrows():
            distance = self.haversine(
                row['lng_restaurant'],
                row['lat_restaurant'],
                row['lng_client'],
                row['lat_client']
            )
            distances.append(distance)

        courier_merge_data['distance'] = distances
        courier_merge_data['time_in_route'] = courier_merge_data['time_complete'] - courier_merge_data['time_pick']
        courier_merge_data['km_h'] = courier_merge_data['distance'] * 60 * 60 / courier_merge_data['time_in_route']

        courier_merge_data.to_csv(courier_merge_data_file_path)
        return courier_merge_data

    def haversine(self, lon1, lat1, lon2, lat2):
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km

    def generate_couriers_speed_data(self):
        result = list()

        couriers = self.data.groupby('courier')

        for courier_id, data_courier in couriers:
            # if len(data_courier) < 20:
            #     continue

            path = 'data/courier-speed/%d.csv' % (int(courier_id))
            data_courier.to_csv(path)

            result.append({
                "courierId": courier_id,
                "itemCounts": len(data_courier),
                "path": path,
            })

        return AnyResult(result)
    def get_couriers(self):
        couriers = self.data['courier'].value_counts()
        print couriers.head()
        couriers_data = list()
        # for courier in couriers:
        #     couriers_data.append({
        #         "": courier[]
        #     })
        return AnyResult(couriers.as_matrix())

    def get_courier_speed(self, courier_id):
        model = self.__load_courier_speed_model(courier_id)
        x = self.__to_nested_list(range(0, 24 * 60 * 60, 10 * 60))
        y = model.predict(x).tolist()

        for idx, val in enumerate(y):
            time = x[idx][0]
            x[idx][0] = '%02d:%02d' % ((time / 60 / 60) % 24, (time / 60) % 60)
            x[idx].append(val)

        return AnyResult(x)

    def get_average_time(self):
        result = list()
        arr = np.arange(0.5, 10.0, 0.1)
        for distance in arr:
            obj = self.__get_average_time_by_distance(distance)
            result.append(obj)
        return AnyResult(result)

    def __get_average_time_by_distance(self, distance):
        data = self.data
        data = data[data['time_in_route'] > 4 * 60]
        data = data[data['distance'] >= distance]
        data = data[data['distance'] < (distance + 0.1)]
        return {
            "mean" : data['time_in_route'].mean(),
            "count": len(data),
            "distance": distance,
        }

    def __load_courier_speed_model(self, courier_id):
        path = 'model/courier-speed/knn-%d.pkl' % (int(courier_id))
        if os.path.isfile(path):
            return joblib.load(path)
        self.__train_cooking_speed_model(path, courier_id)
        return joblib.load(path)

    def __train_cooking_speed_model(self, path, courier_id):
        data = self.__load_courier_speed_data(courier_id)
        data = data[data['distance'] > 1]
        data = data[data['time_in_route'] > 4 * 60]

        if data is None:
            return False
        x = self.__to_nested_list(data['time'])
        y = data['km_h'].as_matrix()
        knn = neighbors.KNeighborsRegressor(n_neighbors=len(x) / 6, weights='uniform')
        knn.fit(x, y)
        joblib.dump(knn, path)
        return True

    def __load_courier_speed_data(self, courier_id):
        path = 'data/courier-speed/%d.csv' % (int(courier_id))
        if not os.path.isfile(path):
            return None
        return pandas.read_csv(path)

    def __to_nested_list(self, arr):
        data = []
        for item in arr:
            data.append([item])
        return data

from math import radians, cos, sin, asin, sqrt

import pandas

from data_result import AnyResult


class Courier:
    def __init__(self):
        self.client_address = pandas.read_csv('data/client-address.csv')
        self.restaurants_address = pandas.read_csv('data/restaurants-address.csv')
        self.orders = pandas.read_csv('data/orders.csv')
        self.data = self.merge_data()

    def merge_data(self):
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

        data.to_csv('data/merge-data.csv')

        for index, row in data.iterrows():
            distance = self.haversine(
                row['lng_restaurant'],
                row['lat_restaurant'],
                row['lng_client'],
                row['lat_client']
            )
            row['distance'] = distance
            # todo: remove
            print index, distance
        return data

    def haversine(self, lon1, lat1, lon2, lat2):
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km

    def get_couriers(self):
        couriers = self.orders['Driver'].value_counts()
        print couriers.head()
        couriers_data = list()
        # for courier in couriers:
        #     couriers_data.append({
        #         "": courier[]
        #     })
        return AnyResult(couriers.as_matrix())
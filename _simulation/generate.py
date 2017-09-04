import pandas


class Generate:

    def __init__(self):
        pass
        self.client_address = pandas.read_csv('../data/client-address.csv')
        self.restaurants_address = pandas.read_csv('../data/restaurants-address.csv')
        self.orders = pandas.read_csv('../data/orders.csv')
        self.order_items = pandas.read_csv('../data/order-items.csv')

    def _get_date(self):
        return [
            (1475179200, '2016_08_30'),
            (1480017600, '2016_11_25'),
            (1478203200, '2016_11_04'),
            (1477598400, '2016_10_28'),
            (1477944000, '2016_11_01'),
        ]

    def _format_orders_date(self):
        trans_date = self.orders.groupby('TransDate')\
            .count()\
            .reset_index(name='count')\
            .sort_values(['count'], ascending=False)
        trans_date.head(5)

    def start(self):
        for (trans_date, name) in self._get_date():
            # order, datetime, lat, lng, lat_restaurant, lng_restaurant, items
            current_data = []
            skip_count = 0
            i = 0
            for index, row in self.orders[self.orders['TransDate'] == trans_date].iterrows():
                order_id = row['ID']
                date_time = row['TimeStart']
                customer_id = row['Customer']
                restaurant_id = row['Restaurant']
                customer = self.client_address[self.client_address['ID'] == customer_id]
                if len(customer) != 1:
                    skip_count += 1
                    continue
                lat = customer.iloc[0]['lat']
                lng = customer.iloc[0]['lng']
                restaurant = self.restaurants_address[self.restaurants_address['ID'] == restaurant_id]
                if len(restaurant) != 1:
                    skip_count += 1
                    continue
                lat_restaurant = restaurant.iloc[0]['lat']
                lng_restaurant = restaurant.iloc[0]['lng']
                i += 1
                # print "%d lat: %s lng: %s lat_restaurant: %s lng_restaurant: %s " % (i, str(lat), str(lng), str(lat_restaurant), str(lng_restaurant))
                # print row['lat']
                # print row['lng']
                # print row['lat_restaurant']
                # print row['lng_restaurant']
                current_data.append({
                    'datetime': date_time,
                    'lat': lat,
                    'lng': lng,
                    'lat_restaurant': lat_restaurant,
                    'lng_restaurant': lng_restaurant,
                })
            print name
            print "order", i
            print "skip", skip_count




def main():
    generate = Generate()
    generate.start()


if __name__ == "__main__":
    main()

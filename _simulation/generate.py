# import pandas
#
#
# class Generate:
#
#     def __init__(self):
#         pass
#         self.restaurants_address = pandas.read_csv('../data/restaurants-address.csv')
#         self.orders = pandas.read_csv('../data/orders.csv')
#         # self.order_items = pandas.read_csv('../data/order-items.csv')
#
#     def _get_date(self):
#         return [
#             (1475179200, '2016_08_30'),
#             (1480017600, '2016_11_25'),
#             (1478203200, '2016_11_04'),
#             (1477598400, '2016_10_28'),
#             (1477944000, '2016_11_01'),
#         ]
#
#     def _format_orders_date(self):
#         trans_date = self.orders.groupby('TransDate')\
#             .count()\
#             .reset_index(name='count')\
#             .sort_values(['count'], ascending=False)
#         trans_date.head(5)
#
#     def start(self):
#         for (trans_date, name) in self._get_date():
#             current_data = []
#
#             order, datetime, lat, lng, lat_restaurant, lng_restaurant
#             for index, row in self.orders[self.orders['TransDate'] == trans_date].iterrows():
#                 print row['ID']
#                 print row['TimeStart']
#             current_data
#             print trans_date
#             print name
#             print current_data.head()
#
#
#
#
#
# def main():
#     generate = Generate()
#     generate.start()
#
#
# if __name__ == "__main__":
#     main()

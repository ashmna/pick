import pandas
from datetime import datetime, timedelta
from util import haversine
from service import restaurant, courier

class Pick:
    def __init__(self):
        self.orders = pandas.DataFrame()
        self.couriers = pandas.DataFrame()

    def courier_enable(self, courier_id):
        courier_obj = self.__get_courier_by_id(courier_id)
        courier_obj['status'] = "wait"

    def courier_disable(self, courier_id):
        courier_obj = self.__get_courier_by_id(courier_id)
        courier_obj['status'] = "away"

    def courier_busy(self, courier_id, order_id):
        courier_obj = self.__get_courier_by_id(courier_id)
        courier_obj['status'] = "busy"
        courier_obj['order_id'] = order_id

    def courier_move(self, courier_id, lat, lng):
        courier_obj = self.__get_courier_by_id(courier_id)
        courier_obj['lat'] = lat
        courier_obj['lng'] = lng

    def __get_courier_by_id(self, courier_id):
        matrix = self.couriers[self.couriers['id'] == courier_id].as_matrix()
        if len(matrix) == 1:
            return matrix[0]
        courier_obj = {
            'courier_id': courier_id
        }
        # todo add more info
        self.couriers.append(courier_obj)
        return courier_obj


    def add_order(self):
        order_data = {}
        order_data.start_datetime = datetime.now()
        order_data.week_day = order_data.start_datetime.weekday()
        order_data.restaurant_id = 1
        order_data.items = [
            {"id": 1, "count": 1},
            {"id": 2, "count": 1},
            {"id": 3, "count": 2},
        ]
        order_data.address_client = ""
        order_data.lat_client = 40.183333
        order_data.lng_client = 44.516667
        order_data.lat_restaurant = 40.183333
        order_data.lng_restaurant = 44.516667

        return self.orders.append(order_data)


    def get_courier_for_order(self, order_id):
        order = self.__get_order_by_id(order_id)
        estimated_cooking_time = self.__get_meal_complete_time(order)

        estimated_cooked_datetime = order.start_datetime + timedelta(seconds=estimated_cooking_time)

        couriers = self.__get_free_couriers(order, estimated_cooked_datetime, 3 * 60)
        t = estimated_cooked_datetime.time()
        time_seconds = t.hour * 60 * 60 + t.minute * 60 + t.second
        couriers = self.__get_free_couriers_at_time(couriers, time_seconds, 3 * 60)


        order.start_date
        order.week_day

    def __get_free_couriers_at_time(self, couriers, date_time, additional_time):
        filtered_couriers = couriers[couriers['estimated_times'] <= date_time + additional_time]
        if len(filtered_couriers) == 0:
            return self.__get_free_couriers_at_time(couriers, date_time, additional_time * 2)
        return filtered_couriers

    def __get_free_couriers(self, order, date_time, additional_time):
        estimated_times = list()
        distances = list()
        t = date_time.time()
        time_seconds = t.hour * 60 * 60 + t.minute * 60 + t.second
        for index, row in self.couriers.iterrows():
            courier_id = row['courier_id']

            if row['status'] == "away":
                distances.append(-1)
                estimated_times.append(-1)
            elif row['status'] == "busy":
                couriers_order = self.__get_order_by_id(row['order_id'])

                distance = haversine(
                    couriers_order['lng_restaurant'],
                    couriers_order['lat_restaurant'],
                    order['lng_client'],
                    order['lat_client']
                )
                distances.append(distance)
                speed = courier.estimate_courier_speed(courier_id, time_seconds)
                estimated_time = distance / speed
                estimated_times.append(estimated_time + additional_time)
            elif row['status'] == "wait":
                distance = haversine(
                    row['lng'],
                    row['lat'],
                    order['lng_client'],
                    order['lat_client']
                )
                distances.append(distance)

                speed = courier.estimate_courier_speed(courier_id, time_seconds)
                estimated_time = distance / speed
                estimated_times.append(estimated_time)


        couriers = self.couriers.copy()
        couriers['distances'] = distances
        couriers['estimated_times'] = estimated_times
        return couriers[couriers['status'] != "away"]

    def __get_order_by_id(self, order_id):
        matrix = self.orders.loc[[order_id]].as_matrix()
        if len(matrix) == 1:
            return matrix[0]
        return {}

    def __get_meal_complete_time(self, order):
        estimated_cooking_time = 0
        for item in order.items:
            item_cooking_time = restaurant.estimate_cooking_time(
                order.week_day,
                order.start_time,
                order.restaurant_id,
                item
            )
            if item_cooking_time > estimated_cooking_time:
                estimated_cooking_time = item_cooking_time

        return estimated_cooking_time

    def get_state(self):






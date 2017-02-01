import copy
from datetime import datetime, timedelta

from data_result import DataResult, AnyResult
from service import restaurant, courier
from util import haversine, filter_object


class Pick:
    def __init__(self):
        self.orders = list()
        self.couriers = {}

    def courier_enable(self, courier_id):
        courier_obj = self.__get_courier_by_id(courier_id)
        courier_obj['status'] = "wait"
        return AnyResult(courier_obj)

    def courier_disable(self, courier_id):
        courier_obj = self.__get_courier_by_id(courier_id)
        courier_obj['status'] = "away"
        return AnyResult(courier_obj)

    def courier_busy(self, courier_id, order_id):
        courier_obj = self.__get_courier_by_id(courier_id)
        courier_obj['status'] = "busy"
        courier_obj['order_id'] = order_id
        return AnyResult(courier_obj)

    def courier_move(self, courier_id, lat, lng):
        courier_obj = self.__get_courier_by_id(courier_id)
        courier_obj['lat'] = lat
        courier_obj['lng'] = lng
        return AnyResult(courier_obj)

    def __get_courier_by_id(self, courier_id):
        courier_id = int(courier_id)
        if self.couriers.has_key(courier_id):
            return self.couriers[courier_id]

        courier_obj = {
            'courier_id': courier_id,
            'status': "away",
            'lat': 0,
            'lng': 0,
            'order_id': 0
        }
        self.couriers[courier_id] = courier_obj
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
        order_data.courier_id = 0
        order_data.distance = haversine(
            order_data.lng_restaurant,
            order_data.lat_restaurant,
            order_data.lng_client,
            order_data.lat_client
        )

        estimated_cooking_time = self.__get_meal_complete_time(order_data)

        estimated_cooked_datetime = order_data.start_datetime + timedelta(seconds=estimated_cooking_time)
        order_data.estimated_cooked_datetime = estimated_cooked_datetime

        return self.orders.append(order_data)

    def get_courier_for_order(self, order_id):
        order = self.__get_order_by_id(order_id)

        couriers = self.__get_free_couriers(order, order.estimated_cooked_datetime, 3 * 60)
        t = order.estimated_cooked_datetime.time()
        time_seconds = t.hour * 60 * 60 + t.minute * 60 + t.second

        if ~self.__is_time_to_choose_courier(couriers, time_seconds):
            return None
        couriers = self.__get_free_couriers_at_time(couriers, time_seconds, 3 * 60)
        couriers = self.__calculate_arrive_time(couriers, order.distance, time_seconds)
        matrix = couriers.as_matrix()
        return matrix[0]

    def __calculate_arrive_time(self, couriers, distance, time_seconds):
        arrive_time = list()
        for index, row in couriers.iterrows():
            courier_id = row['courier_id']
            speed = courier.estimate_courier_speed(courier_id, time_seconds)
            arrive_time.append(distance / speed)

        courier['arrive_time'] = arrive_time
        return courier.sort(['arrive_time'])

    def __is_time_to_choose_courier(self, couriers, time_seconds):
        filtered_couriers = filter_object(couriers, lambda r: r['estimated_times'] <= time_seconds)
        if len(filtered_couriers) == 0:
            return True

        return len(filtered_couriers) / len(couriers) * 100 <= 50

    def __get_free_couriers_at_time(self, couriers, date_time, additional_time):
        filtered_couriers = filter_object(couriers, lambda r: r['estimated_times'] <= date_time + additional_time)
        if len(filtered_couriers) == 0:
            return self.__get_free_couriers_at_time(couriers, date_time, additional_time * 2)
        return filtered_couriers

    def __get_free_couriers(self, order, date_time, additional_time):
        t = date_time.time()
        time_seconds = t.hour * 60 * 60 + t.minute * 60 + t.second

        couriers = copy.deepcopy(self.couriers)

        for courier_id in couriers:
            row = couriers[courier_id]

            if row['status'] == "away":
                row['distance'] = -1
                row['estimated_time'] = -1
            elif row['status'] == "busy":
                couriers_order = self.__get_order_by_id(row['order_id'])

                distance = haversine(
                    couriers_order['lng_restaurant'],
                    couriers_order['lat_restaurant'],
                    order['lng_client'],
                    order['lat_client']
                )
                speed = courier.estimate_courier_speed(courier_id, time_seconds)
                estimated_time = distance / speed
                row['distance'] = distance
                row['estimated_time'] = estimated_time + additional_time
            elif row['status'] == "wait":
                distance = haversine(
                    row['lng'],
                    row['lat'],
                    order['lng_client'],
                    order['lat_client']
                )
                speed = courier.estimate_courier_speed(courier_id, time_seconds)
                estimated_time = distance / speed
                row['distance'] = distance
                row['estimated_time'] = estimated_time

        return filter_object(couriers, lambda r: r['status'] != "away")

    def __get_order_by_id(self, order_id):
        order_id = int(order_id)
        if len(self.orders) > order_id:
            return self.orders[order_id]
        return {}

    @staticmethod
    def __get_meal_complete_time(order):
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
        return DataResult(self.orders)

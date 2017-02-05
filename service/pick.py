import copy
from datetime import datetime, timedelta

from data_result import AnyResult
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

    def courier_complete_order(self, courier_id):
        courier_obj = self.__get_courier_by_id(courier_id)
        if courier_obj['order_id'] != 0:
            self.__done_order(courier_obj['order_id'])
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

    def add_order(self, order_data):
        # order_data = {}
        order_data['start_datetime'] = datetime.now()
        order_data['week_day'] = order_data['start_datetime'].weekday()
        # order_data.restaurant_id = 1
        # order_data.items = [
        #     {"id": 1, "count": 1},
        #     {"id": 2, "count": 1},
        #     {"id": 3, "count": 2},
        # ]
        # order_data.address_client = ""
        # order_data.lat_client = 40.183333
        # order_data.lng_client = 44.516667
        # order_data.lat_restaurant = 40.183333
        # order_data.lng_restaurant = 44.516667
        order_data['courier_id'] = 0
        order_data['distance'] = haversine(
            float(order_data['lng_restaurant']),
            float(order_data['lat_restaurant']),
            float(order_data['lng_client']),
            float(order_data['lat_client'])
        )

        estimated_cooking_time = self.__get_meal_complete_time(order_data)

        estimated_cooked_datetime = order_data['start_datetime'] + timedelta(seconds=estimated_cooking_time)
        order_data['estimated_cooked_datetime'] = estimated_cooked_datetime
        order_data['order_id'] = len(self.orders)
        order_data['status'] = "ToDo"

        self.orders.append(order_data)
        return AnyResult({'order_id': len(self.orders) - 1})

    def get_courier_for_order(self, order_id):
        order = self.__get_order_by_id(order_id)

        t = order['estimated_cooked_datetime'].time()
        time_seconds = t.hour * 60 * 60 + t.minute * 60 + t.second
        now = datetime.now().time()
        now_time_seconds = now.hour * 60 * 60 + now.minute * 60 + now.second
        time_seconds -= now_time_seconds

        couriers = self.__get_free_couriers(order, datetime.now(), 3 * 60)

        if len(couriers) == 0:
            return None

        if not self.__is_time_to_choose_courier(couriers, time_seconds):
            return None
        couriers = self.__get_free_couriers_at_time(couriers, time_seconds, 3 * 60)
        couriers = self.__calculate_arrive_time(couriers, order['distance'], now_time_seconds, datetime.now().weekday())
        min_arrive_time = 0
        min_courier = None
        for courier_id in couriers:
            courier = couriers[courier_id]
            if min_arrive_time == 0 or courier['arrive_time'] < min_arrive_time:
                min_arrive_time = courier['arrive_time']
                min_courier = courier

        return self.__get_courier_by_id(min_courier['courier_id'])

    def __done_order(self, order_id):
        order = self.__get_order_by_id(order_id)
        courier = self.__get_courier_by_id(order['courier_id'])
        order['status'] = "Done"
        courier['status'] = "wait"
        courier['lat'] = order['lat_client']
        courier['lng'] = order['lng_client']

    def __set_courier_for_order(self, courier_obj, order):
        if courier_obj is None:
            return
        from service import courier
        now = datetime.now().time()
        now_time_seconds = now.hour * 60 * 60 + now.minute * 60 + now.second

        order['courier_id'] = courier_obj['courier_id']
        courier_obj['order_id'] = order['order_id']
        courier_obj['status'] = "busy"
        speed = courier.estimate_courier_speed(courier_obj['courier_id'], now_time_seconds, datetime.now().weekday())
        arrive_time = (order['distance'] * 2.0) / 2 / speed * 60 * 60
        courier_obj['estimated_complete_datetime'] = order['estimated_cooked_datetime'] + timedelta(seconds=arrive_time)
        order['estimated_complete_datetime'] = courier_obj['estimated_complete_datetime']
        order['status'] = "InProgress"

    def __calculate_arrive_time(self, couriers, distance, time_seconds, week_day):
        from service import courier
        for courier_id in couriers:
            row = couriers[courier_id]
            courier_id = row['courier_id']
            speed = courier.estimate_courier_speed(courier_id, time_seconds, week_day)
            row['arrive_time'] = (distance * 2.0) / 2 / speed * 60 * 60

        return couriers

    def __is_time_to_choose_courier(self, couriers, time_seconds):
        wait_couriers = filter_object(couriers, lambda r: r['status'] == "wait")
        filtered_couriers = filter_object(couriers, lambda r: r['estimated_time'] <= time_seconds)
        if len(wait_couriers) == 0:
            return False
        if len(filtered_couriers) == 0:
            return True

        return float(len(filtered_couriers)) / float(len(wait_couriers)) * 100 <= 50

    def __get_free_couriers_at_time(self, couriers, date_time, additional_time):
        filtered_couriers = filter_object(couriers, lambda r: r['estimated_time'] <= date_time + additional_time)
        if len(filtered_couriers) == 0:
            return self.__get_free_couriers_at_time(couriers, date_time, additional_time * 2)
        return filtered_couriers

    def __get_free_couriers(self, order, date_time, additional_time):
        from service import courier
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
                    float(couriers_order['lng_restaurant']),
                    float(couriers_order['lat_restaurant']),
                    float(order['lng_client']),
                    float(order['lat_client'])
                )
                speed = courier.estimate_courier_speed(courier_id, time_seconds, date_time.weekday())
                estimated_time = (distance * 2.0) / 2 / speed * 60 * 60
                row['distance'] = distance
                t = row['estimated_complete_datetime'].time()
                estimated_complete_time_seconds = t.hour * 60 * 60 + t.minute * 60 + t.second
                if estimated_complete_time_seconds < time_seconds:
                    estimated_complete_time_seconds += 24 * 60 * 60
                at = estimated_complete_time_seconds - time_seconds
                row['estimated_time'] = at + estimated_time + additional_time
            elif row['status'] == "wait":
                distance = haversine(
                    float(row['lng']),
                    float(row['lat']),
                    float(order['lng_client']),
                    float(order['lat_client'])
                )
                speed = courier.estimate_courier_speed(courier_id, time_seconds, date_time.weekday())
                estimated_time = (distance * 2.0) / 2 / speed * 60 * 60
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
        from service import restaurant
        estimated_cooking_time = 0
        for item in order['items']:
            t = order['start_datetime'].time()
            time_seconds = t.hour * 60 * 60 + t.minute * 60 + t.second

            item_cooking_time = restaurant.estimate_cooking_time(
                order['restaurant_id'],
                item['id'],
                time_seconds,
                order['week_day']
            )
            if item_cooking_time > estimated_cooking_time:
                estimated_cooking_time = item_cooking_time

        return estimated_cooking_time

    def get_state(self):
        # todo: move out
        orders = copy.deepcopy(self.orders)
        orders = sorted(orders, key=lambda ff: ff['estimated_cooked_datetime'])
        for order_copy in orders:
            order = self.__get_order_by_id(order_copy['order_id'])
            if order['courier_id'] != 0:
                continue
            courier = self.get_courier_for_order(order['order_id'])
            self.__set_courier_for_order(courier, order)

        data = list()
        for courier_id in self.couriers:
            row = self.couriers[courier_id]
            if row['status'] == "away":
                continue
            tooltip = 'Courier: %s<br>\nlat: %s, lng: %s,<br>\nStatus: "%s"<br>\nOrderID: %s' % (str(row['courier_id']), str(row['lat']), str(row['lng']), str(row['status']), str(row['order_id']))
            key = '%s-%s-%s' % (str(row['lat']), str(row['lng']), str(row['status']))
            id = 'c-%s' % (str(courier_id))
            if row['status'] == "busy":
                tooltip = 'Complete: %s<br>\n' % str(row['estimated_complete_datetime']) + tooltip
            data.append((
                float(row['lat']),
                float(row['lng']),
                tooltip,
                row['status'],
                id,
                key,
            ))
        restaurants = {}
        for order_id, row in enumerate(self.orders):
            if row['status'] == "Done":
                continue
            if not (row['restaurant_id'] in restaurants):
                restaurants[row['restaurant_id']] = {
                    'restaurant_id': row['restaurant_id'],
                    'orders_count': 0,
                    'orders_have_courier': 0,
                    'lat': row['lat_restaurant'],
                    'lng': row['lng_restaurant'],
                }
            restaurants[row['restaurant_id']]['orders_count'] += 1
            status = "customer_wait"
            if row['courier_id'] != 0:
                status = "customer_busy"
                restaurants[row['restaurant_id']]['orders_have_courier'] += 1

            tooltip = 'Client: %s<br>\n' % str(" ") \
                      + 'Date Time: %s<br>\n' % str(row['start_datetime']) \
                      + 'Estimated Date Time: %s<br>\n' % str(row['estimated_cooked_datetime']) \
                      + 'lat: %s, lng: %s<br>' % (str(row['lat_client']), str(row['lng_client'])) \
                      + '\nOrderID: %s<br>' % str(order_id) \
                      + '\nCourier: %s' % str(row['courier_id'])
            key = '%s-%s-%s' % (str(row['lat_client']), str(row['lng_client']), status)
            id = 'o-%s' % str(order_id)
            data.append((
                float(row['lat_client']),
                float(row['lng_client']),
                tooltip,
                status,
                id,
                key,
            ))
        for restaurant_id in restaurants:
            row = restaurants[restaurant_id]
            tooltip = 'Restaurant: %s<br>\n %s / %s' % (str(restaurant_id), str(row['orders_have_courier']), str(row['orders_count']))
            key = tooltip
            id = 'r-%s' % str(restaurant_id)
            data.append((
                float(row['lat']),
                float(row['lng']),
                tooltip,
                "restaurant",
                id,
                key,
            ))
        return AnyResult(data)

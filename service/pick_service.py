from datetime import datetime, timedelta

from data_result import AnyResult
from util import haversine, filter_object


class PickService:
    def __init__(self):
        from repository import courier_repository, order_repository, calculation_repository
        self.courier_repository = courier_repository
        self.order_repository = order_repository
        self.calculation_repository = calculation_repository

    def courier_enable(self, partner_id, courier_id):
        courier_obj = self.courier_repository.get_by_id(partner_id, courier_id)
        courier_obj.enable()
        return courier_obj

    def courier_disable(self, partner_id, courier_id):
        courier_obj = self.courier_repository.get_by_id(partner_id, courier_id)
        courier_obj.disable()
        return courier_obj

    # def courier_busy(self, courier_id, order_id):
    #     courier_obj = self.courier_repository.get_by_id(courier_id)
    #     courier_obj.busy(order_id)
    #     return AnyResult(courier_obj)

    def courier_move(self, partner_id, courier_id, lat, lng):
        courier_obj = self.courier_repository.get_by_id(partner_id, courier_id)
        courier_obj.move(lat, lng)
        return courier_obj

    def courier_complete_order(self, partner_id, courier_id):
        courier_obj = self.courier_repository.get_by_id(partner_id, courier_id)
        if courier_obj.order_id:
            order_obj = self.order_repository.get_by_id(courier_obj.partner_id, courier_obj.order_id)
            order_obj.done_order(courier_obj)
        return courier_obj

    def add_order(self, partner_id, order_data):
        order_obj = self.order_repository.create_new_order(partner_id, order_data)
        return order_obj

    def calculate(self, partner_id):
        orders = self.order_repository.get_orders_need_to_pick(partner_id)
        all_couriers = self.courier_repository.get_couriers()
        now = datetime.now().time()
        now_time_seconds = now.hour * 60 * 60 + now.minute * 60 + now.second
        order_to_courier = {}
        orders_ids = list()
        couriers_ids = list()

        for courier_obj in all_couriers:
            courier_obj.clean_upcoming_orders()

        for order_obj in orders:
            orders_ids.append(order_obj.order_id)
            time_seconds = order_obj.get_estimated_cooked_seconds()
            time_seconds -= now_time_seconds
            couriers = self._estimate_restaurant_arrive_time(all_couriers, order_obj, now, 3 * 60)
            if len(couriers) == 0:
                continue
            couriers = self._get_free_couriers_at_time(couriers, time_seconds, 3 * 60)
            couriers = self._calculate_arrive_time(couriers, order_obj.distance)

            min_arrive_time = 0
            min_courier_obj = None
            for courier_obj in couriers:
                if min_arrive_time == 0 or courier_obj.client_arrive_time_second < min_arrive_time:
                    min_arrive_time = courier_obj.client_arrive_time_second
                    min_courier_obj = courier_obj
            if min_courier_obj is not None:
                self._set_upcoming_order(min_courier_obj, order_obj)

        for courier_obj in all_couriers:
            couriers_ids.append(courier_obj.courier_id)
            if courier_obj.has_upcoming_order():
                for index in courier_obj.upcoming_orders:
                    upcoming = courier_obj.upcoming_orders[index]
                    order_to_courier[upcoming.order_id] = {
                        'courier_id': courier_obj.courier_id,
                        'sequence': index + 1,
                        'client_arrive_datetime': courier_obj.client_arrive_datetime,
                    }

        self.calculation_repository.save_data(order_to_courier, orders_ids, couriers_ids)

    @staticmethod
    def _set_upcoming_order(courier_obj, order_obj):
        courier_obj.put_upcoming_order(order_obj.order_id, courier_obj.client_arrive_datetime)
        order_obj.put_pick_history(courier_obj.courier_id, courier_obj.client_arrive_datetime)

    @staticmethod
    def _calculate_arrive_time(couriers, distance):
        from service import courier
        for courier_obj in couriers:

            t = courier_obj.restaurant_arrive_datetime.time()
            time_seconds = t.hour * 60 * 60 + t.minute * 60 + t.second

            speed = courier.estimate_courier_speed(
                courier_obj.partner_id,
                courier_obj.courier_id,
                time_seconds,
                courier_obj.restaurant_arrive_datetime.weekday()
            )
            client_arrive_time_second = distance / speed * 60 * 60
            courier_obj.client_arrive_time_second = time_seconds + client_arrive_time_second
            courier_obj.client_arrive_datetime = courier_obj.restaurant_arrive_datetime + timedelta(seconds=client_arrive_time_second)

        return couriers

    # def __is_time_to_choose_courier(self, couriers, time_seconds):
    #     wait_couriers = filter_object(couriers, lambda r: r['status'] == "wait")
    #     filtered_couriers = filter_object(couriers, lambda r: r['estimated_time'] <= time_seconds)
    #     if len(wait_couriers) == 0:
    #         return False
    #     if len(filtered_couriers) == 0:
    #         return True
    #
    #     return float(len(filtered_couriers)) / float(len(wait_couriers)) * 100 <= 50

    def _get_free_couriers_at_time(self, couriers, time_seconds, additional_time):
        filtered_couriers = filter_object(couriers, lambda obj: obj.restaurant_arrive_time_second <= time_seconds + additional_time)
        if len(filtered_couriers) == 0:
            return self._get_free_couriers_at_time(couriers, time_seconds, additional_time * 2)
        return filtered_couriers

    def _estimate_restaurant_arrive_time(self, couriers, order_obj, date_time, additional_time_seconds):
        from service import courier

        t = date_time.time()
        time_seconds = t.hour * 60 * 60 + t.minute * 60 + t.second

        for courier_obj in couriers:
            if courier_obj.has_upcoming_order():
                last_upcoming_order_info = courier_obj.get_last_upcoming_order_info()
                couriers_order = self.order_repository.get_by_id(courier_obj.partner_id, last_upcoming_order_info.order_id)
                distance = haversine(
                    couriers_order.lng_client,
                    couriers_order.lat_client,
                    order_obj.lng_restaurant,
                    order_obj.lat_restaurant
                )

                estimated_complete_datetime = last_upcoming_order_info.client_arrive_datetime
                t = estimated_complete_datetime.time()
                estimated_complete_seconds = t.hour * 60 * 60 + t.minute * 60 + t.second

                if estimated_complete_seconds < time_seconds:
                    estimated_complete_seconds += 24 * 60 * 60

                estimate_speed_at_datetime = date_time + timedelta(seconds=(estimated_complete_seconds - time_seconds))
                t = estimate_speed_at_datetime.time()
                estimate_speed_at_seconds = t.hour * 60 * 60 + t.minute * 60 + t.second

                speed = courier.estimate_courier_speed(
                    courier_obj.partner_id,
                    courier_obj.courier_id,
                    estimate_speed_at_seconds,
                    estimate_speed_at_datetime.weekday()
                )

                at = estimated_complete_seconds - time_seconds
                estimated_second = at + additional_time_seconds + (distance / speed * 60 * 60)
                courier_obj.restaurant_arrive_time_second = estimated_second
                courier_obj.restaurant_arrive_datetime = date_time + timedelta(seconds=estimated_second)
            elif courier_obj.is_busy():
                couriers_order = self.order_repository.get_by_id(courier_obj.partner_id, courier_obj.order_id)
                distance = haversine(
                    couriers_order.lng_client,
                    couriers_order.lat_client,
                    order_obj.lng_restaurant,
                    order_obj.lat_restaurant
                )

                estimated_complete_seconds = order_obj.get_estimated_complete_seconds()

                if estimated_complete_seconds < time_seconds:
                    estimated_complete_seconds += 24 * 60 * 60

                estimate_speed_at_datetime = date_time + timedelta(seconds=(estimated_complete_seconds - time_seconds))
                t = estimate_speed_at_datetime.time()
                estimate_speed_at_seconds = t.hour * 60 * 60 + t.minute * 60 + t.second

                speed = courier.estimate_courier_speed(
                    courier_obj.partner_id,
                    courier_obj.courier_id,
                    estimate_speed_at_seconds,
                    estimate_speed_at_datetime.weekday()
                )

                at = estimated_complete_seconds - time_seconds
                estimated_second = at + additional_time_seconds + (distance / speed * 60 * 60)
                courier_obj.restaurant_arrive_time_second = estimated_second
                courier_obj.restaurant_arrive_datetime = date_time + timedelta(seconds=estimated_second)
            elif courier_obj.is_wait():
                distance = haversine(
                    courier_obj.lng,
                    courier_obj.lat,
                    order_obj.lng_restaurant,
                    order_obj.lat_restaurant
                )
                speed = courier.estimate_courier_speed(
                    courier_obj.partner_id,
                    courier_obj.courier_id,
                    time_seconds,
                    date_time.weekday()
                )
                estimated_second = additional_time_seconds + (distance / speed * 60 * 60)
                courier_obj.restaurant_arrive_time_second = estimated_second
                courier_obj.restaurant_arrive_datetime = date_time + timedelta(seconds=estimated_second)
        return couriers

    def get_state(self):
        return AnyResult([])

    # def get_state(self):
    #     # todo: move out
    #     orders = copy.deepcopy(self.orders)
    #     orders = sorted(orders, key=lambda ff: ff['estimated_cooked_datetime'])
    #     for order_copy in orders:
    #         order = self.__get_order_by_id(order_copy['order_id'])
    #         if order['courier_id'] != 0:
    #             continue
    #         courier = self.get_courier_for_order(order['order_id'])
    #         self.__set_courier_for_order(courier, order)
    #
    #     data = list()
    #     for courier_id in self.couriers:
    #         row = self.couriers[courier_id]
    #         if row['status'] == "away":
    #             continue
    #         tooltip = 'Courier: %s<br>\nlat: %s, lng: %s,<br>\nStatus: "%s"<br>\nOrderID: %s' % (str(row['courier_id']), str(row['lat']), str(row['lng']), str(row['status']), str(row['order_id']))
    #         key = '%s-%s-%s' % (str(row['lat']), str(row['lng']), str(row['status']))
    #         id = 'c-%s' % (str(courier_id))
    #         if row['status'] == "busy":
    #             tooltip = 'Complete: %s<br>\n' % str(row['estimated_complete_datetime']) + tooltip
    #         data.append((
    #             float(row['lat']),
    #             float(row['lng']),
    #             tooltip,
    #             row['status'],
    #             id,
    #             key,
    #         ))
    #     restaurants = {}
    #     for order_id, row in enumerate(self.orders):
    #         if row['status'] == "Done":
    #             continue
    #         if not (row['restaurant_id'] in restaurants):
    #             restaurants[row['restaurant_id']] = {
    #                 'restaurant_id': row['restaurant_id'],
    #                 'orders_count': 0,
    #                 'orders_have_courier': 0,
    #                 'lat': row['lat_restaurant'],
    #                 'lng': row['lng_restaurant'],
    #             }
    #         restaurants[row['restaurant_id']]['orders_count'] += 1
    #         status = "customer_wait"
    #         if row['courier_id'] != 0:
    #             status = "customer_busy"
    #             restaurants[row['restaurant_id']]['orders_have_courier'] += 1
    #
    #         tooltip = 'Client: %s<br>\n' % str(" ") \
    #                   + 'Date Time: %s<br>\n' % str(row['start_datetime']) \
    #                   + 'Estimated Date Time: %s<br>\n' % str(row['estimated_cooked_datetime']) \
    #                   + 'lat: %s, lng: %s<br>' % (str(row['lat_client']), str(row['lng_client'])) \
    #                   + '\nOrderID: %s<br>' % str(order_id) \
    #                   + '\nCourier: %s' % str(row['courier_id'])
    #         key = '%s-%s-%s' % (str(row['lat_client']), str(row['lng_client']), status)
    #         id = 'o-%s' % str(order_id)
    #         data.append((
    #             float(row['lat_client']),
    #             float(row['lng_client']),
    #             tooltip,
    #             status,
    #             id,
    #             key,
    #         ))
    #     for restaurant_id in restaurants:
    #         row = restaurants[restaurant_id]
    #         tooltip = 'Restaurant: %s<br>\n %s / %s' % (str(restaurant_id), str(row['orders_have_courier']), str(row['orders_count']))
    #         key = tooltip
    #         id = 'r-%s' % str(restaurant_id)
    #         data.append((
    #             float(row['lat']),
    #             float(row['lng']),
    #             tooltip,
    #             "restaurant",
    #             id,
    #             key,
    #         ))
    #     return AnyResult(data)

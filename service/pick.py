import pandas

from service import restaurant, courier

class Pick:
    def __init__(self):
        self.orders = pandas.DataFrame()
        self.couriers = pandas.DataFrame()

    def courier_enable(self, courier_id):
        courier = self.__get_courier_by_id(courier_id)
        courier.status = "wait"

    def courier_disable(self, courier_id):
        courier = self.__get_courier_by_id(courier_id)
        courier.status = "away"

    def courier_busy(self, courier_id):
        courier = self.__get_courier_by_id(courier_id)
        courier.status = "busy"

    def __get_courier_by_id(self, courier_id):
        matrix = self.couriers[self.couriers['id'] == courier_id].as_matrix()
        if len(matrix) == 1:
            return matrix[0]
        courier = {}
        # todo add more info
        self.couriers.append(courier)
        return courier


    def add_order(self):
        order_data = {}
        order_data.start_date = 1
        order_data.start_time = 1
        order_data.week_day = 1
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
        order.week_day
        order.start_time




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




from mongoengine import *


class CouriersOrders(Document):
    current_order = DictField()
    upcoming_orders = ListField()

    def __init__(self, current_order, upcoming_orders, *args, **values):
        super(CouriersOrders, self).__init__(*args, **values)
        if current_order:
            self.current_order = current_order.to_dict()
        self.upcoming_orders = upcoming_orders

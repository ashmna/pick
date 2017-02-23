from domain import Order
from datetime import datetime

class OrderRepository:
    def __init__(self):
        pass

    def get_by_id(self, order_id):
        return Order.objects.get(id=order_id)

    def create_new_order(self, data):
        partner_id = 0
        order_obj = Order()
        order_obj.start(partner_id, datetime.now(), data)
        return order_obj

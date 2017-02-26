from domain import Order
from datetime import datetime


class OrderRepository:
    def __init__(self):
        pass

    def get_by_id(self, partner_id, order_id):
        return Order.objects.get(partner_id=partner_id, order_id=order_id)

    def create_new_order(self, partner_id, data):
        order_obj = Order()
        order_obj.start(partner_id, datetime.now(), data)
        return order_obj

from domain import Order
from datetime import datetime


class OrderRepository:
    def __init__(self):
        pass

    def get_by_id(self, partner_id, order_id):
        return Order.objects.get(partner_id=partner_id, order_id=order_id)

    def get_order_list(self, partner_id, skip, limit):
        return Order.objects(partner_id=partner_id)

    def create_new_order(self, partner_id, order_id, data):
        order_obj = Order()
        order_obj.start(partner_id, order_id, datetime.now(), data)
        return order_obj

    def update_order(self, partner_id, order_id, data):
        order_obj = self.get_by_id(partner_id, order_id)
        for key in data:
            if key == 'courier_id':
                order_obj.courier_id = data[key]
            elif key == 'is_courier_picked_manual':
                order_obj.is_courier_picked_manual = data[key]
            elif key == 'items':
                order_obj.items = data[key]
        return self.save(order_obj)

    def get_orders_need_to_pick(self, partner_id):
        return Order.objects(partner_id=partner_id, status='todo').order_by('estimated_cooked_datetime')

    def save(self, order_obj):
        return order_obj.save()

from mongoengine import *


class Calculation(Document):
    partner_id = IntField()
    order_to_courier = DictField()
    orders_ids = ListField()
    couriers_ids = ListField()

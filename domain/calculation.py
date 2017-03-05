from mongoengine import *


class Calculation(Document):
    partner_id = IntField()
    order_to_courier = DictField()

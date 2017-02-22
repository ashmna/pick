from mongoengine import *

connect('pick', host='localhost', username='', password='')


class Courier(Document):
    courier_id = LongField()
    status = StringField(max_length=4)  # away, wait, busy
    lat = LongField()
    lng = LongField()
    order_id = LongField()


class Order:
    order_id = LongField()
    status = StringField(max_length=10)  # ToDo, InProgress, Done
    start_datetime = DateTimeField()
    estimated_cooked_datetime = DateTimeField()
    estimated_complete_datetime = DateTimeField()
    lat_restaurant = LongField()
    lng_restaurant = LongField()
    lat_client = LongField()
    lng_client = LongField()
    distance = LongField()
    courier_id = LongField()
    restaurant_id = LongField()
    items = ListField()  # {id, count}

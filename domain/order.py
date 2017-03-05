from datetime import datetime, timedelta

from mongoengine import *

from util import haversine


class Order(Document):
    partner_id = LongField()
    order_id = LongField()
    status = StringField(max_length=10)
    start_datetime = DateTimeField()
    estimated_cooked_datetime = DateTimeField()
    estimated_complete_datetime = DateTimeField()
    lat_restaurant = FloatField()
    lng_restaurant = FloatField()
    lat_client = FloatField()
    lng_client = FloatField()
    distance = FloatField()
    courier_id = LongField()
    restaurant_id = LongField()
    items = ListField()  # {id, count}
    complete_datetime = DateTimeField()
    pick_history = ListField()

    def start(self, partner_id, date_time, data):
        self.order_id = int((date_time - datetime(1970, 1, 1)).total_seconds())
        self.partner_id = partner_id
        self.status = "todo"
        self.courier_id = 0
        self.start_datetime = date_time

        self.lat_restaurant = float(data['lat_restaurant'])
        self.lng_restaurant = float(data['lng_restaurant'])
        self.lat_client = float(data['lat_client'])
        self.lng_client = float(data['lng_client'])

        self.distance = haversine(
            self.lng_restaurant,
            self.lat_restaurant,
            self.lng_client,
            self.lat_client
        )

        self.restaurant_id = long(data['restaurant_id'])
        self.items = list()
        for item in data['items']:
            self.items.append({
                'id': long(item['id']),
                'count': int(item['count']),
            })

        estimated_cooking_time = self.estimate_cooking_time()
        self.estimated_cooked_datetime = self.start_datetime + timedelta(seconds=estimated_cooking_time)

        self.save()

    def done_order(self, courier_obj):
        courier_obj.move(self.lat_client, self.lng_client)
        courier_obj.complete_order()

        self.status = "done"
        self.complete_datetime = datetime.now()
        self.save()

    def set_courier(self, courier_id, estimated_complete_datetime):
        self.status = "inProgress"
        self.courier_id = courier_id
        self.estimated_complete_datetime = estimated_complete_datetime
        self.save()

    def get_start_seconds(self):
        t = self.start_datetime.time()
        return t.hour * 60 * 60 + t.minute * 60 + t.second

    def get_estimated_cooked_seconds(self):
        t = self.estimated_cooked_datetime.time()
        return t.hour * 60 * 60 + t.minute * 60 + t.second

    def get_estimated_complete_seconds(self):
        t = self.estimated_complete_datetime.time()
        return t.hour * 60 * 60 + t.minute * 60 + t.second

    def estimate_cooking_time(self):
        from service import restaurant
        estimated_cooking_time = 0
        for item in self.items:
            item_cooking_time = restaurant.estimate_cooking_time(
                self.partner_id,
                self.restaurant_id,
                item['id'],
                self.get_start_seconds(),
                self.start_datetime.weekday()
            )
            if item_cooking_time > estimated_cooking_time:
                estimated_cooking_time = item_cooking_time

        return estimated_cooking_time

    def put_pick_history(self, courier_id, client_arrive_datetime):
        if not self.pick_history:
            self.pick_history = list()
        self.pick_history.append({
            'date_time': datetime.now(),
            'courier_id': courier_id,
            'client_arrive_datetime': client_arrive_datetime,
        })
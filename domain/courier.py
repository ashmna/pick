from mongoengine import *


class Courier(Document):
    partner_id = LongField()
    courier_id = LongField()
    status = StringField(max_length=4)  # away, wait, busy
    lat = FloatField()
    lng = FloatField()
    order_id = LongField()

    def enable(self):
        self.status = "wait"
        self.save()

    def disable(self):
        self.status = "away"
        self.save()

    def pick(self, order_id):
        self.status = "busy"
        self.order_id = order_id
        self.save()

    def move(self, lat, lng):
        self.lat = float(lat)
        self.lng = float(lng)
        self.save()
        # todo emit event

    def complete_order(self):
        self.status = "wait"
        self.order_id = 0
        self.save()

    def is_busy(self):
        return self.status == "busy"

    def is_wait(self):
        return self.status == "wait"


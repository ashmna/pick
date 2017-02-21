from datetime import datetime, timedelta


class Courier:
    courier_id = 0
    status = "away"  # away, wait, busy
    lat = 0
    lng = 0
    order_id = 0


class Order:
    order_id = 0
    status = "ToDo"  # ToDo, InProgress, Done
    start_datetime = None
    estimated_cooked_datetime = None
    estimated_complete_datetime = None
    lat_restaurant = 0
    lng_restaurant = 0
    lat_client = 0
    lng_client = 0
    distance = 0
    courier_id = 0
    restaurant_id = 0
    items = []  # {id, count}


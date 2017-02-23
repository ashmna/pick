from domain import Courier


class CourierRepository:
    def __init__(self):
        pass

    def get_by_id(self, courier_id):
        # courier_obj = Courier.objects.get(courier_id=courier_id)
        # if courier_obj is None:
            # todo: add partner id
        courier_obj = Courier()
        courier_obj.courier_id = courier_id
        courier_obj.order_id = 0
        courier_obj.move(0, 0)
        return courier_obj


    def get_couriers(self):
        return Courier.objects(status_in=["wait", "busy"])


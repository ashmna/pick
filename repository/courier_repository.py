from domain import Courier


class CourierRepository:
    def __init__(self):
        pass

    def get_by_id(self, partner_id, courier_id):
        try:
            return Courier.objects.get(partner_id=partner_id, courier_id=courier_id)
        except Courier.DoesNotExist:
            courier_obj = Courier()
            courier_obj.partner_id = partner_id
            courier_obj.courier_id = courier_id
            courier_obj.order_id = 0
            courier_obj.move(0, 0)
            return courier_obj

    def get_couriers(self, partner_id):
        return Courier.objects(partner_id=partner_id, status__in=["wait", "busy"])

    def save(self, courier_obj):
        return courier_obj.save()

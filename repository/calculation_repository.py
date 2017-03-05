from domain import Calculation


class CalculationRepository:
    def __init__(self):
        pass

    def save_data(self, partner_id, order_to_courier, orders_ids, couriers_ids):
        try:
            calculation_obj = Calculation.objects.get(partner_id=partner_id)
        except Calculation.DoesNotExist:
            calculation_obj = Calculation()
            calculation_obj.partner_id = partner_id
        calculation_obj.order_to_courier = order_to_courier
        calculation_obj.orders_ids = orders_ids
        calculation_obj.couriers_ids = couriers_ids
        calculation_obj.save()
        return calculation_obj

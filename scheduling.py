import threading

from service import token_service, pick_service


def set_interval(func, partner_id, sec):
    def func_wrapper():
        func(partner_id)
        set_interval(func, partner_id, sec)

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def schedule():
    for token_obj in token_service.get_all():
        sec = token_obj.settings['calculation_velocity']
        pick_service.calculate(token_obj.partner_id)
        set_interval(lambda partner_id: pick_service.calculate(partner_id), token_obj.partner_id, sec)

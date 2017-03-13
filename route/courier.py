from bottle import request

from api import api
from service import courier, token_service


@api.route('/courier/gen', method='GET')
def generate_couriers_speed_data():
    partner_id = token_service.get_partner_id(request)
    return courier.generate_couriers_speed_data().to_json()


@api.route('/courier/list', method='GET')
def get_couriers():
    partner_id = token_service.get_partner_id(request)
    return courier.get_couriers().to_json()


@api.route('/courier/speed/<courier_id:float>', method='GET')
def get_courier_speed(courier_id):
    partner_id = token_service.get_partner_id(request)
    return courier.get_courier_speed(courier_id).to_json()


@api.route('/courier/average', method='GET')
def get_average_time():
    partner_id = token_service.get_partner_id(request)
    return courier.get_average_time().to_json()

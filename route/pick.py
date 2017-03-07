import json

from bottle import route, request

from service import pick_service, token_service


@route('/pick/courier/enable/<courier_id:float>', method='GET')
def courier_enable(courier_id):
    partner_id = token_service.get_partner_id(request)
    return pick_service.courier_enable(partner_id, courier_id).to_json()


@route('/pick/courier/disable/<courier_id:float>', method='GET')
def courier_disable(courier_id):
    partner_id = token_service.get_partner_id(request)
    return pick_service.courier_disable(partner_id, courier_id).to_json()


# @route('/pick/courier/busy/<courier_id:float>', method='GET')
# def courier_busy(courier_id):
#     partner_id = token_service.get_partner_id(request)
#     return pick_service.courier_busy(partner_id, courier_id).to_json()


@route('/pick/courier/move/<courier_id:float>', method='GET')
def courier_move(courier_id):
    partner_id = token_service.get_partner_id(request)
    lat = request.query['lat']
    lng = request.query['lng']
    return pick_service.courier_move(partner_id, courier_id, lat, lng).to_json()


@route('/pick/courier/complete/<courier_id:float>', method='GET')
def courier_complete_order(courier_id):
    partner_id = token_service.get_partner_id(request)
    return pick_service.courier_complete_order(partner_id, courier_id).to_json()


@route('/pick/order/add/<order_id:float>', method='POST')
def add_order(order_id):
    partner_id = token_service.get_partner_id(request)
    data = json.load(request.body)
    return pick_service.add_order(partner_id, order_id, data['order']).to_json()


@route('/pick/order/courier/<order_id:float>', method='GET')
def get_courier_for_order(order_id):
    partner_id = token_service.get_partner_id(request)
    return pick_service.get_courier_for_order(partner_id, order_id).to_json()


@route('/pick/order/courier/<order_id:float>/<courier_id:float>', method='PUT')
def set_courier_for_order(order_id, courier_id):
    partner_id = token_service.get_partner_id(request)
    return pick_service.set_courier_for_order(partner_id, order_id, courier_id).to_json()


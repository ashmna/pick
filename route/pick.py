from bottle import route, request

from service import pick


@route('/pick/courier/enable/<courier_id:float>', method='GET')
def courier_enable(courier_id):
    return pick.courier_enable(courier_id).to_json()


@route('/pick/courier/disable/<courier_id:float>', method='GET')
def courier_disable(courier_id):
    return pick.courier_disable(courier_id).to_json()


@route('/pick/courier/busy/<courier_id:float>', method='GET')
def courier_busy(courier_id):
    return pick.courier_busy(courier_id).to_json()


@route('/pick/courier/move/<courier_id:float>', method='GET')
def courier_move(courier_id):
    lat = request.query['lat']
    lng = request.query['lng']
    return pick.courier_move(courier_id, lat, lng).to_json()


@route('/pick/order', method='PUT')
def generate_couriers_speed_data():
    # todo add order parameters
    order_id = pick.add_order()
    data = pick.get_courier_for_order(order_id)
    return data.to_json()


@route('/courier/list', method='GET')
def get_restaurants():
    return courier.get_couriers().to_json()


@route('/courier/speed/<courier_id:float>', method='GET')
def get_restaurants(courier_id):
    return courier.get_courier_speed(courier_id).to_json()


@route('/courier/average', method='GET')
def get_average_time():
    return courier.get_average_time().to_json()

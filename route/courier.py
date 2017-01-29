from bottle import route

from service import courier


@route('/courier/gen', method='GET')
def generate_couriers_speed_data():
    return courier.generate_couriers_speed_data().to_json()


@route('/courier/list', method='GET')
def get_couriers():
    return courier.get_couriers().to_json()


@route('/courier/speed/<courier_id:float>', method='GET')
def get_courier_speed(courier_id):
    return courier.get_courier_speed(courier_id).to_json()


@route('/courier/average', method='GET')
def get_average_time():
    return courier.get_average_time().to_json()

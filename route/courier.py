from bottle import route

from service import courier


@route('/courier/list', method='GET')
def get_restaurants():
    return courier.get_couriers().to_json()


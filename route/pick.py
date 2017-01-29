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


@route('/pick/state', method='GET')
def get_state():
    return pick.get_state().to_json()

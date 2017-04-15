import bottle

import route
from config import config_app
from scheduling import schedule

app = bottle.Bottle()


@app.route('/', method='GET')
def root_response():
    return bottle.HTTPResponse(status=200)


@bottle.route('/<:re:.*>', method='OPTIONS')
def enable_cross_generic_route():
    add_cross_headers()


@bottle.hook('after_request')
def enable_cross_after_request_hook():
    add_cross_headers()


def add_cross_headers():
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    bottle.response.headers['Access-Control-Allow-Methods'] = \
        'GET, POST, PUT, OPTIONS'
    bottle.response.headers['Access-Control-Allow-Headers'] = \
        'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


if __name__ == '__main__':
    schedule()
    from api import api

    @api.route('/<:re:.*>', method='OPTIONS')
    def enable_cross_generic_route():
        add_cross_headers()

    @api.hook('after_request')
    def enable_cross_after_request_hook():
        add_cross_headers()
    app.mount(config_app.prefix, api)
    app.run(host=config_app.host, port=config_app.port)
    route.start()

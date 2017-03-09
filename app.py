import bottle

import route
from config import config_app
from scheduling import schedule


@bottle.route('/<:re:.*>', method='OPTIONS')
def enable_cors_generic_route():
    add_cors_headers()


@bottle.hook('after_request')
def enable_cors_after_request_hook():
    add_cors_headers()


def add_cors_headers():
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    bottle.response.headers['Access-Control-Allow-Methods'] = \
        'GET, POST, PUT, OPTIONS'
    bottle.response.headers['Access-Control-Allow-Headers'] = \
        'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


if __name__ == '__main__':
    schedule()
    app = bottle.app()
    app.run(host=config_app.host, port=config_app.port, prefix=config_app.prefix)
    route.start()


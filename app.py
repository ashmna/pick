import bottle

import route


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
    app = bottle.app()
    app.run(host='0.0.0.0', port=3000)
    route.start()

import bottle

api = bottle.Bottle()


@api.get('/')
def root_response():
    bottle.HTTPResponse(status=200)


@api.hook('after_request')
def headers():
    bottle.response.content_type = 'application/json'

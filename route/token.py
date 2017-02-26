import json

from bottle import route, request

from service import token_service


@route('/token/gen', method='PUT')
def generate_token():
    data = json.load(request.body)
    # data.partner_id
    return token_service.generate_token(data).to_json()


@route('/token/<token>', method='GET')
def get_data(token):
    return token_service.get_data(token).to_json()

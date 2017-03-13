import json

from bottle import request, HTTPResponse

from api import api
from service import token_service


@api.route('/token/gen', method='PUT')
def generate_token():
    data = json.load(request.body)
    # data.partner_id
    return token_service.generate_token(data).to_json()


@api.route('/token/<token>', method='GET')
def get_data(token):
    return token_service.get_data(token).to_json()


@api.route('/test', method='GET')
def root_response():
    return HTTPResponse(status=200, body='test')


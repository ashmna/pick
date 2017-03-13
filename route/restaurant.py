from bottle import request

from api import api
from service import restaurant, token_service


@api.route('/restaurant/gen', method='GET')
def generate_cooking_speed_data():
    partner_id = token_service.get_partner_id(request)
    return restaurant.generate_cooking_speed_data().to_json()


@api.route('/restaurant/list', method='GET')
def get_restaurants():
    partner_id = token_service.get_partner_id(request)
    return restaurant.get_restaurants().to_json()


@api.route('/restaurant/items/<restaurant_id:float>', method='GET')
def get_restaurant_items(restaurant_id):
    partner_id = token_service.get_partner_id(request)
    return restaurant.get_restaurant_items(restaurant_id).to_json()


@api.route('/restaurant/item/cooking-speed/<restaurant_id:float>/<item_number:float>', method='GET')
def get_restaurant_item_cooking_speed(restaurant_id, item_number):
    partner_id = token_service.get_partner_id(request)
    return restaurant.get_restaurant_item_cooking_speed(restaurant_id, item_number).to_json()

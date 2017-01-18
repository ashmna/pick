from bottle import route

from service import restaurant


@route('/restaurant/gen', method='GET')
def generate_cooking_speed_data():
    return restaurant.generate_cooking_speed_data().to_json()


@route('/restaurant/list', method='GET')
def get_restaurants():
    return restaurant.get_restaurants().to_json()


@route('/restaurant/items/<restaurant_id:float>', method='GET')
def get_restaurant_items(restaurant_id):
    return restaurant.get_restaurant_items(restaurant_id).to_json()


@route('/restaurant/item/cooking-speed/<restaurant_id:float>/<item_number:float>', method='GET')
def get_restaurant_item_cooking_speed(restaurant_id, item_number):
    return restaurant.get_restaurant_item_cooking_speed(restaurant_id, item_number).to_json()

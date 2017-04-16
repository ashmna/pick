from mongoengine import *

from calculation import Calculation
from config import config_mongodb
from courier import Courier
from order import Order
from token import Token
from couriers_orders import CouriersOrders

connect(
    db=config_mongodb.name,
    alias='default',
    host=config_mongodb.host,
    port=config_mongodb.port,
    username=config_mongodb.username,
    password=config_mongodb.password,
)

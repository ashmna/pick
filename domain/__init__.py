from mongoengine import *

from calculation import Calculation
from config import config_mongodb
from courier import Courier
from order import Order
from token import Token

connect(
    config_mongodb.name,
    host=config_mongodb.host,
    port=config_mongodb.port,
    username=config_mongodb.username,
    password=config_mongodb.password,
)

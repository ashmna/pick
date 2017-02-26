from mongoengine import *

from courier import Courier
from order import Order
from token import Token

connect('pick', host='localhost', username='', password='')

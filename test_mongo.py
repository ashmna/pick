from config import config_mongodb
from mongoengine import *


class Test(Document):
    data = DictField()

connect(
    db=config_mongodb.name,
    alias='default',
    host=config_mongodb.host,
    port=config_mongodb.port,
    username=config_mongodb.username,
    password=config_mongodb.password,
)


test = Test()
test.data = {'some': 'test data'}
test.save()

print 'ok'

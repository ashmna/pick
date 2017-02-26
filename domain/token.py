from mongoengine import *


class Token(Document):
    partner_id = IntField()
    token = StringField(max_length=64)

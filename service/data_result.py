from json import dumps

from bottle import response


class DataResult:
    data = []

    def __init__(self, data):
        self.data = data

    def to_json(self):
        response.content_type = 'application/json'
        return self.data.to_json(orient='records')


class AnyResult:
    def __init__(self, data):
        self.data = data

    def to_json(self):
        response.content_type = 'application/json'
        return dumps(self.data)

from json import dumps


class DataResult:
    data = []

    def __init__(self, data):
        self.data = data

    def to_json(self):
        return self.data.to_json(orient='records')


class AnyResult:
    def __init__(self, data):
        self.data = data

    def to_json(self):
        return dumps(self.data)

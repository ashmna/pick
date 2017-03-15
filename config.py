import os
print os.environ['HOME']


class ConfigMongoDB():
    name = 'pick'
    host = 'localhost'
    port = 27017
    username = ''
    password = ''

    def __init__(self):
        if 'MONGODB_NAME' in os.environ:
            self.name = os.environ['MONGODB_NAME']
        if 'MONGODB_HOST' in os.environ:
            self.host = os.environ['MONGODB_HOST']
        if 'MONGODB_PORT' in os.environ:
            self.port = os.environ['MONGODB_PORT']
        if 'MONGODB_USERNAME' in os.environ:
            self.username = os.environ['MONGODB_USERNAME']
        if 'MONGODB_PASSWORD' in os.environ:
            self.password = os.environ['MONGODB_PASSWORD']
        print 'MONGODB_NAME %s' % str(self.name)
        print 'MONGODB_HOST %s' % str(self.host)
        print 'MONGODB_PORT %s' % str(self.port)
        print 'MONGODB_USERNAME %s' % str(self.username)
        print 'MONGODB_PASSWORD%s' % str(self.password)


class ConfigApp():
    host = '0.0.0.0'
    port = 3000
    prefix = '/api/v1/'

    def __init__(self):
        if 'APP_HOST' in os.environ:
            self.name = os.environ['APP_HOST']
        if 'APP_PORT' in os.environ:
            self.host = os.environ['APP_PORT']
        if 'APP_PREFIX' in os.environ:
            self.prefix = os.environ['APP_PREFIX']
        print 'APP_HOST %s' % str(self.name)
        print 'APP_PORT %s' % str(self.host)
        print 'APP_PREFIX %s' % str(self.prefix)


config_mongodb = ConfigMongoDB()
config_app = ConfigApp()

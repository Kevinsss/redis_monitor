import json

import redis

import config


class MockRedis(object):

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 6379
        # self.password = 'pwd'
        self.client = redis.StrictRedis(host=self.host, port=self.port, db=0)

    def mock_setnx(self):
        for i in range(0,20000):
            self.client.setex('test' + str(i), 100, 'value' + str(i))

    def mock_del(self):
        for i in range(0, 20000):
            self.client.delete('test' + str(i))

if __name__ == '__main__':
    mock_redis = MockRedis()
    # mock_redis.mock_del()
    mock_redis.mock_setnx()
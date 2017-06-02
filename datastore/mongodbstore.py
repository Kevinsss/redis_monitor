import contextlib

import pymongo
import json
import config
from pymongo import MongoClient
from bson import json_util as jsonb


class MongodbStore(object):
    def __init__(self):
        store_mongodb = json.loads(config.STORE_MONGODB)
        self.host = store_mongodb['host']
        self.port = store_mongodb['port']
        self.database = store_mongodb['database']
        self.password = store_mongodb.get('password')
        self.conn = MongoClient(host=self.host, port=self.port)
        self.db = self.conn.get_database(self.database)

    def set_command_count(self, optime, cmdcount, ip):
        data = {'optime': optime, 'cmdcount': cmdcount, 'ip': ip}
        with contextlib.closing(self.conn) as c:
            db = c.get_database(self.database)
            result = db.command_count.insert(data)
            return result

    def set_memory_count(self, optime, used_memory, peak_memory, ip):
        data = {'optime': optime, 'used_memory': used_memory, 'peak_memory': peak_memory, 'ip': ip}
        with contextlib.closing(self.conn) as c:
            db = c.get_database(self.database)
            result = db.memory_count.insert(data)
            return result

    def set_info(self, optime, info_dict, ip):
        data = {'optime': optime, 'info': json.dumps(info_dict), 'ip': ip}
        with contextlib.closing(self.conn) as c:
            db = c.get_database(self.database)
            result = db.info.insert(data)
            return result

    def get_ip(self):
        with contextlib.closing(self.conn) as c:
            db = c.get_database(self.database)
            results = db.command_count.distinct('ip')
            return json.dumps(results)

    def get_command_count(self, ip, start, end):
        with contextlib.closing(self.conn) as c:
            db = c.get_database(self.database)
            results = db.command_count.find({'ip': ip, 'optime': {'$gte': start, '$lte': end}},
                                             {'_id': 0, 'ip': 0}).sort([("optime", pymongo.ASCENDING)])
            results = list(results)
            return jsonb.dumps(results)

    def get_memory_count(self, ip, start, end):
        with contextlib.closing(self.conn) as c:
            db = c.get_database(self.database)
            results = db.memory_count.find({'ip': ip, 'optime': {'$gte': start, '$lte': end}},
                                           {'_id': 0, 'ip': 0}).sort([("optime", pymongo.ASCENDING)])
            results = list(results)
            return jsonb.dumps(results)

    def get_info(self, ip):
        with contextlib.closing(self.conn) as c:
            db = c.get_database(self.database)
            results = db.info.find({'ip': ip}, {'_id': 0, 'ip': 0}).sort([("optime", pymongo.DESCENDING)]).skip(0).limit(1)

            print results[0]['info']
            return results[0]['info']

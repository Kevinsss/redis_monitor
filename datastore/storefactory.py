import config
import mongodbstore
#from datastore import mysqlstore


class RedisDataStoreFactory(object):

    @staticmethod
    def get_store():
        data_store_type = config.DATA_STORE_TYPE

        if data_store_type == 'mongodb':
            return mongodbstore.MongodbStore()
        if data_store_type == 'redis':
            return redisstore.RedisStore()
        if data_store_type == 'mysql':
            return mysqlstore.MysqlStore()

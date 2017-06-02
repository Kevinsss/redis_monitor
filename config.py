# config.py

# the redis that you want to monitor, could be multi-redis
# example:
# [
#     {
#         "host": "127.0.0.1",
#         "port": 6379
#     },
#     {
#         "host": "127.0.0.1",
#         "port": 6379,
#         "password": "redis-password"
#     }
# ]
REDIS_SERVERS = '''
[
    {
        "host": "127.0.0.1",
        "port": 6379
    }
]
'''

# data store type,  'mysql', 'mongodb'
DATA_STORE_TYPE = 'mongodb'

# store redis info to mongodb
STORE_MONGODB = '''
{
    "host": "127.0.0.1",
    "port": 27017,
    "database": "redis_monitor"
}   
'''


# store redis info to mysql
STORE_MYSQL = '''
{
    "host": "127.0.0.1",
    "port": 33306,
    "username": "root",
    "password": "root",
    "database": "redis_monitor"
}   
'''

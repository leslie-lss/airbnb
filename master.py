# -*- coding:utf-8 -*-

import redis
from pymongo import MongoClient

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def get_id_from_mongo():
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.airbnb
    my_set = db.list_1126
    new_set = db.room_1126_1747
    for x in my_set.find():
        print(x['_id'])
        if new_set.find({'_id': x['_id']}).count() > 0:
            continue
        r.rpush('url', x['_id'])
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

if __name__ == '__main__':
    get_id_from_mongo()

print("success0")
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import redis
import Config as conf
class RedisClient(object):
    def __init__(self, name, namespace='aicyber', **redis_kwargs):
        self.__db = redis.Redis(**redis_kwargs)
        #self.__db.flushdb()
        self.key = '%s:%s' % (namespace, name)
        print '...redis...key: %s' % self.key

    def qsize(self):
        return self.__db.llen(self.key)

    def empty(self):
        return self.qsize() == 0

    def put(self, item):
        self.__db.rpush(self.key, item)

    def has_name(self,name):
        return self.__db.hexists(self.key,name)

    def hset(self, name, value):
        self.__db.hset(self.key, name, value)

    def hget(self, name):
        return self.__db.hget(self.key, name)

    def hgetall(self):
        return self.__db.hgetall(self.key)

    def hsize(self):
        return self.__db.hlen(self.key)

    def hremove(self, name):
        return self.__db.hdel(self.key, name)

    def hremoveall(self):
        dict = self.hgetall()
        for k, v in dict.items():
            self.__db.hdel(self.key, k)
# ===========================================================================
print '---REDIS_DB---',conf.REDIS_DB
print '---redis_host--',conf.REDIS_HOST
r = RedisClient(conf.REDIS_DB, host=conf.REDIS_HOST, password='aicyber', port=conf.REDIS_PORT, db=0)
if __name__ == '__main__':


    r.hset('uuid--0','15900282168')
    r.hset('uuid--1', '18002017665')
    r.hset('uuid--2', '13022297501')
    # #
    # print redis.hgetall()
    # #
    map = r.hgetall()
    print type(map), map
    for k, v in map.items():
        print k, v
    #     # redis.hremove(k)
    #
    #     # print redis.hgetall()
    #     # print redis.hsize()
    # print r.has_name('uuid--2')
    # print r.hget('uuid--2')

    print '==================================='
    print r.hget('uuid--1')






















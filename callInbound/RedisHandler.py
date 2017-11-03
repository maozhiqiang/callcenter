#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import redis
import Md5Utils
import Config as conf
class RedisClient(object):
    """Simple Queue with Redis Backend"""

    def __init__(self, name, namespace='aicyber', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db = redis.Redis(**redis_kwargs)
        self.__db.flushdb()
        self.key = '%s:%s' % (namespace, name)
        print '...redis...key: %s' % self.key

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.__db.rpush(self.key, item)
#=======================setcache=============================
    """
            Set the value at key ``name`` to ``value``

            ``ex`` sets an expire flag on key ``name`` for ``ex`` seconds.

            ``px`` sets an expire flag on key ``name`` for ``px`` milliseconds.

            ``nx`` if set to True, set the value at key ``name`` to ``value`` if it
                does not already exist.

            ``xx`` if set to True, set the value at key ``name`` to ``value`` if it
                already exists.
            """
    #set(self, name, value, ex=None, px=None, nx=False, xx=False)
    def setCache(self,name,value):
        self.__db.setex(name,value)

    # def getCache(self,name):
    #     self.__db.get(s)

# ===========================================================================

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

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)
        if item:
            item = item[1]
        return item

    def delete_key(self):
        self.__db.delete(self.key)

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)

    def remove_value_lrem(self, value):
        """ 从队列中删除指定的value"""
        print '....................remove: %s' % value
        return self.__db.lrem(self.key, value)

    def get_value_list(self, queueSize):
        item_list = self.__db.lrange(self.key, 0, queueSize)
        return item_list
print '---REDIS_DB---',conf.REDIS_DB
print '---redis_host--',conf.REDIS_HOST
r = RedisClient(conf.REDIS_DB, host='127.0.0.1', password='aicyber', port=conf.REDIS_PORT, db=0)
if __name__ == '__main__':
    ss_flag = '85f235e449606ad09e07e2f49fd2ebce' + '_' + '我们楼盘是津南区，比邻天嘉湖大道4A级景区，南八里台镇政府附近，这边您知道的吧？'
    key = Md5Utils.get_md5_value(ss_flag)
    print '****',key
    r.hset(key,'我们楼盘是津南区，比邻天嘉湖大道4A级景区，南八里台镇政府附近，这边您知道的吧？')
    print '****'

    # r.hset('uuid--1', '18002017665')
    # r.hset('uuid--2', '13022297501')
    # # #
    # # print redis.hgetall()
    # #
    # map = r.hgetall()
    # print type(map), map
    # for k, v in map.items():
    #     print k, v
    #     # redis.hremove(k)
    #
    #     # print redis.hgetall()
    #     # print redis.hsize()
    # print r.has_name('uuid--2')
    # print r.hget('uuid--2')

    print '==================================='

    # r.setCache('name','value132')
    print r.hget('uuid--0')























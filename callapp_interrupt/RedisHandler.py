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
        # self.__db.flushdb()
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
# =======================setcache=============================
        """
                Set the value at key ``name`` to ``value``

                ``ex`` sets an expire flag on key ``name`` for ``ex`` seconds.

                ``px`` sets an expire flag on key ``name`` for ``px`` milliseconds.

                ``nx`` if set to True, set the value at key ``name`` to ``value`` if it
                    does not already exist.

                ``xx`` if set to True, set the value at key ``name`` to ``value`` if it
                    already exists.
                """

        # set(self, name, value, ex=None, px=None, nx=False, xx=False)
        def setCache(self, name, value):
            self.__db.setex()
# =======================setcache=============================

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

r = RedisClient(conf.REDIS_DB, host=conf.REDIS_HOST, password='aicyber', port=conf.REDIS_PORT, db=0)
if __name__ == '__main__':


    # r.hset('uuid--0','15900282168')
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
    text = '5566'
    ss_key = Md5Utils.get_md5_value(text)
    print ss_key
    if r.has_name(ss_key):
        print  "this key is exit"
        r.hset(ss_key, 'mnt/asr/asr/test_5566.wav')
        print  r.hget(ss_key)


















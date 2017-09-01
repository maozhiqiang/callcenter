# -*- encoding: utf-8 -*-
import redis
import time
pool = redis.ConnectionPool(host='121.42.36.138', password='aicyber', port=6379)
r = redis.Redis(connection_pool=pool)
print(r.get('hexm'))
r.setex('hexm', 20, time=3)
print(r.get('hexm'))
time.sleep(2)
print(r.get('hexm'))
time.sleep(1)
print(r.get('hexm'))

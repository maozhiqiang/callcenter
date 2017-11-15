#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# import database
# from time import time
# db = database.PSQL()
# lst = [str(i) for i in range(20)]
# t = time()
# n = 10000
# while n:
#     key = lst.pop(0)
#     db.get_conn(key)
#     data = db.query(table='vshop_order',
#                       columns=['id', 'order_no', 'state'],
#                       # order_by='-id',
#                       limit=1)
#     n -= 1
#     db.put_conn(key)
#     lst.append(key)
# print(time() - t)
import psycopg2.pool
from time import time

t = time()
n = 100
lst = [str(i) for i in range(20)]
simple_conn_pool = psycopg2.pool.SimpleConnectionPool(5, 200, host = '118.190.166.165',port = 5432,user = 'postgres', password = 'z8asuidn', dbname = 'postgres')
while n:
    key = lst.pop(0)
    conn = simple_conn_pool.getconn(key)
    cur = conn.cursor()
    cur.execute("select * from fs_call where cust_number = '15900282168'")
    info =cur.fetchall()
    print info
    n -= 1
    lst.append(key)
print(time() - t)
simple_conn_pool.closeall()


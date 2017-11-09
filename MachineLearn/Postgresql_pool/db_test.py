#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import database
from time import time
db = database.PSQL()
lst = [str(i) for i in range(20)]
t = time()
n = 10000
while n:
    key = lst.pop(0)
    db.get_conn(key)
    data = db.query(table='vshop_order',
                      columns=['id', 'order_no', 'state'],
                      # order_by='-id',
                      limit=1)
    n -= 1
    db.put_conn(key)
    lst.append(key)
print(time() - t)
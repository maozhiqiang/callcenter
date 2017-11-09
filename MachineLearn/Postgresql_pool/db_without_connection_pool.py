import database
from time import time
t = time()
n = 10000
db = database.PSQL()
while n:
    db.get_conn()
    data = db.query(table='vshop_order',
                      columns=['id', 'order_no', 'state'],
                      order_by='-id',
                      limit=1)
    n -= 1
print(time() - t)
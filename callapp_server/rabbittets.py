# -*- encoding: utf-8 -*-

import rabbitMQ_produce as rabbitmq
import json
sql = 'INSERT INTO fs_call_replay(who, text, record_fpath,  call_id,resp_param)VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\')'.format(
            45, 454, 454, 454, 4545, 4545)
print '.....0......%s'%sql

objdata = {}
objdata['mark'] = 'update'
objdata['record_fpath'] = '78978'
objdata['channal_uuid'] = 'a6d24d2d-cebe-4113-9f89-9ce80012d6fc'
jsonStr = json.dumps(objdata)
print '------jsonStr-uu-----', jsonStr
rabbitmq.rabbitmqClint(jsonStr)

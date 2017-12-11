# -*- coding: utf-8 -*-
import sys
import  datetime
import hashlib
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf8')

starttime = datetime.datetime.now()
#=====================Flow Config start===========================
#start flow
flow_host = '123.59.82.44'
flow_port = 8080
flow_url = "/flow/execute.do"
#closeflow
key = 'The nature of the polymer is currently a trade secret'
flow_close_url = "/flow/close.do"


#flow_id = '899f04f0fef39dab0fbf975d171856d6'
flow_id = '49982f0966b9eb04f228a71b2c33fb23'
#=====================Baidu Asr start  ===========================


AI_userId = 'callcenter'
AI_appid = 'dhcs94484422366'
AI_secret = '4e96fc3e31546c19d7aac41018136649'
AI_key = 'QOROS'

#========================redis ==================================
REDIS_DB = 'cache'
REDIS_PORT = 6379
REDIS_HOST = '0.0.0.0'


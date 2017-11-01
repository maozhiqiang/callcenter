# -*- coding: utf-8 -*-
import sys
import  datetime
import uuid
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf8')

starttime = datetime.datetime.now()

AI_userId = 'callcenter'
AI_appid = 'dhcs94484422366'
AI_secret = '4e96fc3e31546c19d7aac41018136649'
AI_key = 'QOROS'

uid = uuid.uuid1()
uid3 = uuid.uuid3(uuid.NAMESPACE_DNS, AI_key)
# print uuid.uuid1()  # 带参的方法参见Python Doc
# print uuid.uuid3(uuid.NAMESPACE_DNS, str(starttime))
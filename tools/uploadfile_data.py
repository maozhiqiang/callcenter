#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-11-29 下午2:49
# @Author  : Arvin
# @Site    : 
# @File    : uploadfile_data.py
# @Software: PyCharm
#http://101.200.142.165:8010/api/task/_app/my-todo-item/
import httplib

import json
httpClient = None

try:
    # with open('/home/whc/下载/13566359103_in_6_20171123154530.wav', 'rb') as fp:
    #     voice_data = fp.read()
    #     fp.seek(0)
    params = {"number":"15900282168","flow_id":"f2d8d40117c3259e1325e938e1be5625","host_id":1,"replace_data":""}
    httpClient = httplib.HTTPConnection('118.190.166.165', 10090, timeout=30)
    httpClient.request('POST', '/api/task/tocall/',json.dumps(params),headers={'Authorization': 'token b9f9633e86673696fc80e2c44fd46f5f51acc7cb'})

    # response是HTTPResponse对象
    response = httpClient.getresponse()
    print response.status
    print response.reason
    print response.read()
except Exception, e:
    print e
finally:
    if httpClient:
        httpClient.close()


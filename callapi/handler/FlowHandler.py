# -*- coding: UTF-8 -*-
import httplib
import json
import callapi.config as Config
import callapi.common.Md5Utils as md5
from callapi.common.LogUtils import Logger
logger = Logger()
#开始流程
def flowHandler(input,userId,flowId='a599d36c4c7a71ddcc1bc7259a15ac3a'):
    secret = md5.get_sha1_value(flowId + Config.key + userId)
    httpClient = None
    try:
        values = {'secret': secret, 'flow_id': flowId, 'user_id': userId, 'input': input}
        params = json.dumps(values)
        headers = {"Content-type": "application/json"}
        httpClient = httplib.HTTPConnection(Config.flow_host, Config.flow_port, timeout=30)
        httpClient.request("POST", Config.flow_url, params, headers)
        response = httpClient.getresponse()
        if response.status == 200:
            jsonStr = response.read()
            dict = json.loads(jsonStr)
            result = dict
            logger.debug('Flow return ----------%s' % dict)
        else:
            result = {'successful': False, 'message': 'httpclient error'}
            logger.debug('.......httpClient error status : %s'%response.status)
    except Exception, e:
        result = {'successful': False, 'message': 'httpclient exception'}
        logger.debug('.......httpClient exception error  : %s' % e)
    finally:
        if httpClient:
            httpClient.close()
    return result
#结束流程
def closeFlow(userId,flowId):
    secret = md5.get_sha1_value(flowId + Config.key + userId)
    httpClient = None
    try:
        values = {'secret': secret, 'flow_id': flowId, 'user_id': userId}
        params = json.dumps(values)
        headers = {"Content-type": "application/json"}
        httpClient = httplib.HTTPConnection(Config.flow_host, Config.flow_port, timeout=30)
        httpClient.request("POST", Config.flow_close_url, params, headers)
        response = httpClient.getresponse()
        if response.status == 200:
            jsonStr = response.read()
            dict = json.loads(jsonStr)
            logger.debug('Flow close return ----------%s' % dict)
        else:
            logger.debug('.......httpClient error status : %s' % response.status)
    except Exception, e:
        logger.debug('.......httpClient exception error  : %s' % e)
    finally:
        if httpClient:
            httpClient.close()

if __name__ == '__main__':
    result = flowHandler(u'你好', '15900282168')
    # closeFlow('15900282168','a6ae62b9-b5cd-4e3e-9d1f-f77c8f47ad0c')





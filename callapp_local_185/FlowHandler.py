# -*- coding: UTF-8 -*-
import httplib
import json
import Config
import Md5Utils as md5
from LogUtils import Logger
from  PsqlUtils import DBHelper
db = DBHelper()
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
            logger.info('Flow return ----------%s' % dict)
        else:
            result = {'successful': False, 'message': 'httpclient error'}
            logger.info('.......httpClient error status : %s'%response.status)
    except Exception, e:
        result = {'successful': False, 'message': 'httpclient exception'}
        logger.info('.......httpClient exception error  : %s' % e)
    finally:
        if httpClient:
            httpClient.close()
    return result
#结束刘海曾
def closeFlow(userId,channal_uuid):
    list = db.getFlowIdAndAppId(userId,channal_uuid)
    flowId = list[4]
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
            logger.info('Flow close return ----------%s' % dict)
        else:
            logger.info('.......httpClient error status : %s' % response.status)
    except Exception, e:
        logger.info('.......httpClient exception error  : %s' % e)
    finally:
        if httpClient:
            httpClient.close()

if __name__ == '__main__':
    result = flowHandler('而不是拿冠军了', '15900282168')
    # print  result
    # pass
    # closeFlow('15900282168','a6d24d2d-cebe-4113-9f89-9ce80012d6fc')





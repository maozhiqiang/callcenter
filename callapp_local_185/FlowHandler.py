# -*- coding: UTF-8 -*-
import httplib
import json
import Config
import Md5Utils as md5
from LogUtils import Logger
from  PsqlUtils import DBHelper
db = DBHelper()
logger = Logger()

def get2days():
    import datetime
    ntime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    d1 = datetime.datetime.strptime('2018-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(ntime, '%Y-%m-%d %H:%M:%S')
    delta = d1 - d2
    print  '-----', delta.days
    if delta.days > 0:
        print '*****True***********'
        return True
    else:
        print '-----False----------'
        return False

#开始流程
def flowHandler(input,userId,flowId='a599d36c4c7a71ddcc1bc7259a15ac3a'):
    secret = md5.get_sha1_value(flowId + Config.key + userId)
    httpClient = None
    if get2days():
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
                logger.info('.......httpClient error status : %s' % response.status)
        except Exception, e:
            result = {'successful': False, 'message': 'httpclient exception'}
            logger.info('.......httpClient exception error  : %s' % e)
        finally:
            if httpClient:
                httpClient.close()
    else:
        result = {'successful': False, 'message': 'Flow Timeout '}
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
    # get2days()
    result = flowHandler('而不是拿冠军了', '15900282168')
    print  result
    # pass
    # closeFlow('15900282168','a6d24d2d-cebe-4113-9f89-9ce80012d6fc')





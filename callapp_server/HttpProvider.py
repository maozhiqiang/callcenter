# coding=utf-8

import  json
import urllib
import urllib2
import httplib

#开始流程
def asr_APP(file):
    httpClient = None
    try:
        values = {'filename': file}
        params = json.dumps(values)
        headers = {"Content-type": "application/json"}
        httpClient = httplib.HTTPConnection('0.0.0.0',5000, timeout=30)
        httpClient.request("POST", '/asr', params, headers)
        response = httpClient.getresponse()
        if response.status == 200:
            jsonStr = response.read()
            dict = json.loads(jsonStr)
            result = dict
        else:
            result = {'successful': False, 'message': 'httpclient error'}
    except Exception, e:
        result = {'successful': False, 'message': 'httpclient exception'}
    finally:
        if httpClient:
            httpClient.close()
    return result


if __name__ == '__main__':
    pcmFileName = '/mnt/asr/15880114563_in_4_20170721150453.wav'
    print asr_APP(pcmFileName)
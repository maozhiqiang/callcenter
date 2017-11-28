#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-11-28 上午10:28
# @Author  : Arvin
# @Site    : 
# @File    : SinoVoice.py
# @Software: PyCharm
import time
import json
import httplib

def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

class Transaction(object):
    def __init__(self):
        self.custom_timers = {}
        self.devkey = '3fcafa0ce5601914e25e6a516d5126d3'
        self.x_app_key = '245d54fe'
        # self.x_task_config = 'capkey=asr.cloud.freetalk,audioformat=pcm8k16bit,domain=telecom'
        self.x_task_config = 'capkey=asr.cloud.freetalk,audioformat=pcm16k16bit,domain=common'
        self.x_sdk_version = '5.0'
        self.content_type = 'application/json;charset=utf-8'
        self.x_result_format = 'json'

    def asr_text(self,audio):
        startTime = time.time()
        dct ={}
        x_request_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dct['x-app-key'] = self.x_app_key
        dct['x-udid'] = '101:1234567890'
        dct['x-request-date'] = x_request_date
        dct['x-task-config'] = self.x_task_config
        dct['x-session-key'] = md5(x_request_date + self.devkey)
        dct['x-sdk-version'] = self.x_sdk_version
        dct['x-result-format'] = self.x_result_format
        with open(audio, 'rb') as fp:
            voice_data = fp.read()
            fp.seek(0)
        conn = httplib.HTTPConnection("api.hcicloud.com:8880")
        headers =dct
        start = time.time()
        conn.request("POST", "http://api.hcicloud.com:8880/asr/Recognise", body=voice_data,headers=headers)
        response = conn.getresponse()
        data = response.read()
        endTime = time.time()
        conn.close()
        print 'SinoVoice ASR Time :%s \nresult :%s' % ((endTime-startTime),data)
        info = json.loads(data)
        result = {}
        if info['ResponseInfo']['ErrorNo'] == '0' and info['ResponseInfo']['ResCode'] == 'Success':
            result['ret'] = 0
            result['result'] =  info['ResponseInfo']['Result']['Text']
        else:
            result['ret'] = 1
            result['result'] = None
        return result
trans = Transaction()
if __name__ == '__main__':
    pass
    # file_wav = '/mnt/asr/asr/13821917127_in_4_20171127150608.wav'
    file_wav = '/home/whc/下载/13566359103_in_6_20171123154530.wav'
    print trans.asr_text(file_wav)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import httplib
import demjson
import datetime
from pydub import AudioSegment
class VoiceTools(object):
    def __init__(self):
        self.index = 0
        self.rootPath = '/home/callcenter/recordvoice/{0}/bot_audio/{1}_out_{2}_{3}.wav'
        self.__sessionId = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.url = 'http://106.75.96.130:8090/synthesis'
        self.headers = {"Content-type": "application/json", "Accept": "text/json"}
        self.conn = httplib.HTTPConnection('106.75.96.130:8090')

    #list 交叉拼接
    def joinlist(self,list1,list2):
        result_list = []
        for index1, item in enumerate(list1):
            if index1 % 2 == 0:
                result_list.append(item)
                if len(list2) > 0:
                    result_list.append(list2.pop(0))
            else:
                result_list.append(item)
                if len(list2) > 0:
                    result_list.append(list2.pop(0))
        return  result_list

    #声音拼接
    def voicesynthetic(self,flow_Id,call_number,kwargs):
        objdata = {}
        path = self.rootPath.format(flow_Id,call_number,self.index,self.__sessionId)
        self.index += 1
        try:
            result = AudioSegment.silent(duration=100)
            for value in kwargs:
                result += AudioSegment.from_wav(value)
            result.set_frame_rate(8000).export(path, format="wav")
            objdata['path'] = path
            objdata['success'] = True
            objdata['message'] = "合成成功"
        except Exception as e:
            print e.message
            objdata['path'] = None
            objdata['success'] = False
            objdata['message'] = e.message
        return  json.dumps(objdata)

    #截取指定字符串
    def screen_str(self,text):
        pattern = r"#{(.+?)}#"
        find_list = re.findall(pattern, text)
        return  find_list

    #http接口服务
    def httpClient(self,speakerid, text):
        p = {"voice_type": speakerid, "text": text}
        params = json.dumps(p)
        self.conn.request('POST', self.url, params, self.headers)
        response = self.conn.getresponse()
        if response.status == 200:
            json_data = response.read()
            dict = json.loads(json_data)
            print '*********',dict
            return dict['data']['path']
        else:
            return None


vt = VoiceTools()
if __name__ == '__main__':
    print  vt.httpClient('xn','中信国际8989案例看价位')




#     import re
#     str = '你好啊#{name}#,我是#{address}#'
#     ll = ['/mnt/vice_join/A1.wav','/mnt/vice_join/eval-400000-3.wav','/mnt/vice_join/eval-400000-5.wav']
#     vt = VoiceTools()
#     for num in range(3):
#         result = vt.voicesynthetic("55667788","15900282168",ll)
#
#         print result
    # print vt.screen_str(str)
    # # vt.screen_str(str)
    # list1 = ['A','B','C','D','E']
    # list2 = ['1', '2', '3', '4']
    # r = vt.joinlist(list1,list2)
    # print r

    # llll = []
    # if len(list1) and len(list2):
    #     print "*************************************"
    # for index1, item in enumerate(list1):
    #     if index1%2 == 0:
    #         llll.append(item)
    #         if len(list2)>0:
    #             llll.append(list2.pop(0))
    #     else:
    #         llll.append(item)
    #         if len(list2) > 0:
    #             llll.append(list2.pop(0))
    # print llll
        # print index, item

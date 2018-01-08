#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-1-8 下午4:40
# @Author  : Arvin
# @Site    : 
# @File    : JoinAudio.py
# @Software: PyCharm
import json
import datetime
from pydub import AudioSegment

class VoiceTools(object):
    def __init__(self):
        self.rootPath = '/home/callcenter/recordvoice/{0}/bot_audio/{1}.wav'
        self.__sessionId = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.strs = None

    def voicesynthetic(self,flow_Id,kwargs):
        objdata = {}
        path = self.rootPath.format(flow_Id,self.__sessionId)
        try:
            result = AudioSegment.silent(duration=100)
            for value in kwargs:
                print value
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
        find_list = re.findall(pattern, str)
        print '------ find_list: {0}---O(∩_∩)O---'.format(find_list)
        return  find_list
vt = VoiceTools()
if __name__ == '__main__':
    import re
    # str = '你好啊#{name}#,我是#{address}#'
    # ll = ['/mnt/vice_join/A1.wav','/mnt/vice_join/eval-400000-3.wav','/mnt/vice_join/eval-400000-5.wav']
    # vt = VoiceTools()
    # result = vt.voicesynthetic("55667788",ll)
    #
    # print result









    # vt.screen_str(str)
    list1 = ['A','B','C','D','E']
    list2 = ['1', '2', '3', '4']
    llll = []
    for index1, item in enumerate(list1):
        if index1%2 == 0:
            llll.append(item)
            if len(list2)>0:
                llll.append(list2.pop(0))
        else:
            llll.append(item)
            if len(list2) > 0:
                llll.append(list2.pop(0))
    print llll
        # print index, item

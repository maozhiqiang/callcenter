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

    def voicesynthetic(self,flow_Id,*args):
        objdata = {}
        path = self.rootPath.format(flow_Id,self.__sessionId)
        try:
            result = AudioSegment.silent(duration=100)
            for value in args:
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

if __name__ == '__main__':
    vt = VoiceTools()
    result = vt.voicesynthetic("55667788","/mnt/vice_join/A1.wav","/mnt/vice_join/eval-400000-3.wav","/mnt/vice_join/eval-400000-5.wav","/mnt/vice_join/eval-400000-0.wav")
    print result

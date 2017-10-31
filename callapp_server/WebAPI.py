# -*- coding: utf-8 -*-
import time
import redis
import json
import Config as conf
import base64
import httplib
from pydub import AudioSegment

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#redis做缓存
pool = redis.ConnectionPool(host=conf.REDIS_HOST, password='aicyber', port=6379)
r = redis.Redis(connection_pool=pool)

class WebApi:

    def __init__(self):

        self.requrl = 'http://openapi.openspeech.cn/webapi/iat.do?svc=token'

        self.xpar = "appid=595da0aa"

        # self.getToken()
        # print 'token:',self.getToken()
        return


    def getToken(self):
        x_par_base64 = base64.b64encode(self.xpar.encode(encoding="utf-8")).strip('\n')
        headers = {"X-Par": x_par_base64}
        #conn = httplib.HTTPConnection("openapi.openspeech.cn")
        conn = httplib.HTTPConnection("117.121.21.146")
        #conn = httplib.HTTPConnection(conf.XUNFEI_URL)
        conn.request(method="GET",url=self.requrl,headers = headers)
        response = conn.getresponse()
        res= response.read().decode('utf-8')
        body_base64_decode = base64.b64decode(res.encode(encoding="utf-8"))
        dict = json.loads(body_base64_decode)

        return dict['token']

    def getText(self,file):
        #print 'start ...0..%s'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        wav16file = self.converTowav(file)
        #print 'start ...1..%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        token = r.get("token")
        print '.....redis ......token',token
        if token == None:
            token = self.getToken()
            r.setex("token", token, 7200)
            print 'redis cache  set token  %s'%token
            token = r.get("token")
        requrl = "http://openapi.openspeech.cn/webapi/iat.do?svc=iat&token="+ str(token)+"&aue=raw&ent=sms16k&auf=audio/L16;rate=16000"
        file_data = open(wav16file, 'rb')
        body_base64 = base64.b64encode(file_data.read())
        file_data.close()
        Xpar = "YXBwaWQ9NTk1ZGEwYWE="
        headers = {"Content-Type": "binary", "X-Par": Xpar}
        # conn = httplib.HTTPConnection("openapi.openspeech.cn")
        conn = httplib.HTTPConnection("117.121.21.146")
        #conn = httplib.HTTPConnection(conf.XUNFEI_URL)
        conn.request(method="POST", url=requrl, body=body_base64,headers=headers)
        response = conn.getresponse()
        res = response.read().decode('utf-8')
        body_base64_decode = base64.b64decode(res.encode(encoding="utf-8")).decode()
        print"body_base64decode : {}".format(body_base64_decode)
        info = json.loads(body_base64_decode)
        return info

    def converTowav(self, filename):
        arr = filename.split('.')
        wavfilename = arr[0] + '.wav'
        seg = AudioSegment.from_wav(filename)
        seg = seg.set_frame_rate(16000)
        seg.export(wavfilename, format="wav")
        return wavfilename
vc = WebApi()
if __name__ == "__main__":

    bdr = WebApi()
    start = time.time()
    # result = bdr.getText('/mnt/asr/asr/15900282168_in_4_20170810113514.wav' )    ### 音频文件路径
    result = bdr.getText('/mnt/鼎鼎_vad/shang_voice/013672004641_in_8_20171019180909.wav')  ### 音频文件路径
    end = time.time()
    print end-start

    if result['ret'] == 0:
        print '---------------',result['result']


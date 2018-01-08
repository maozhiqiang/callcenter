# -*- encoding: utf-8 -*-
import datetime
import requests
import wave

class BaiduVoiceClient(object):
    token_cache = [None, datetime.datetime.fromtimestamp(0)]

    def __init__(self, cu_id, api_key, api_secert):
        self.cu_id = cu_id
        self.api_key = api_key
        self.api_secert = api_secert

    def get_token(self):
        _now = datetime.datetime.now()
        _day = (_now - self.token_cache[1]).days
        if self.token_cache[0] and _day < 20:
            return self.token_cache[0]
        params = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secert
        }
        r = requests.get(url='https://openapi.baidu.com/oauth/2.0/token',
                         params=params)
        _json = r.json()
        self.token_cache[0] = _json['access_token']
        self.token_cache[1] = _now
        return self.token_cache[0]

    def tts(self, text, filename):
        print self.get_token()
        params = {
            'tex': text,
            'lan': 'zh',
            'tok': self.get_token(),
            'ctp': 1,
            'cuid': self.cu_id
        }
        r = requests.get(url="http://tsn.baidu.com/text2audio", params=params)
        if r.headers['content-type'] == 'audio/mp3':
            with open(filename, 'wb+') as fp:
                fp.write(r.content)
            return 0
        else:
            return r.json()

    def asr(self, filename):
        with open(filename, 'rb') as fp:
            voice_data = fp.read()
            fp.seek(0)
            wav_reader = wave.open(fp, 'rb')
            sampwidth = wav_reader.getsampwidth()
            framerate = wav_reader.getframerate()
            # print 'in baidu asr:', sampwidth, framerate

        params = {
            'cuid': self.cu_id,
            'token': self.get_token(),
        }
        headers = {
            'Content-Type': 'audio/wav;rate=%s' % framerate,
            'Content-length': str(len(voice_data))
        }
        r = requests.post(url='http://vop.baidu.com/server_api',
                          params=params,
                          data=voice_data,
                          headers=headers)
        return r.json()


bc = BaiduVoiceClient(cu_id='test_python',
                      api_key='92NfxqqrTsTYwwVuiD5kEKGK',
                      api_secert='QPBc3VI716rwOwxWIoE6BgXRtcFqqUWw')



# if __name__ == "__main__":
#     import  time
#     start = time.time()
#     s = "欢迎您的来电，呼叫人工请按 2，呼叫智能客服请按 3，重复收听请按 0!"
#     r = bc.tts(s, '/tmp/11_test_tts.wav')

    # #--------
    # import time
    # for num in range(5):
    #     start = time.time()
    #     # print 'startTime: ',time.time()
    #     file = '/home/python_project/call/static/human_audio/13672004641_in_{0}_20170719174104.wav'.format(num)
    #     r = bc.asr(file)
    #     end = time.time()
    #     print r['result'][0]
    #     print (end-start)
    # #--------
    #a-b
    # file = '/mnt/asr/asr/18522611368_in_5_20171101153938.wav'
    # r = bc.asr(file)
    # print r['result'][0]
    # end = time.time()
    # # print r
    # print (end - start)

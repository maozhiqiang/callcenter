# -*- encoding: utf-8 -*-
import os
import io
import uuid
import wave
import time
import voice_api
import AI_chat
import AI_config
import WebAPI as xunfei_asr
from freeswitch import *
from pydub import AudioSegment
from record_log import RecordLogCLient
import datetime
reload(voice_api)
reload(xunfei_asr)

rc = RecordLogCLient(AI_config.AI_key)

def hangup_hook(session, what):
    consoleLog("info", "hangup hook for %s!!\n\n" % what)
    return


def input_callback(session, what, obj):
    if (what == "dtmf"):
        consoleLog("info", what + " " + obj.digit + "\n")
    else:
        consoleLog("info", what + " " + obj.serialize() + "\n")
    return "pause"


class IVRBase(object):
    STATUS_MAP = {
        'banks_call': u'您好，中国农业银行，请说出您要办理的业务，您可以说：查询信用卡额度、查询开户行。请问，您要办理什么业务？',
        'banks_answer_loop': u'您还有其他问题要咨询我吗？结束请挂机！',
        'banks_answer_fail': u'我没听清，请问您要办理什么业务'

    }
    FINAL_STATUS_KEFU = '100'
    FINAL_STATUS_USER = '200'
    def __init__(self, session, args, status='banks_call'):
        self.session = session
        self.args = args
        self.status = status
        self.in_count = 0
        self.out_count = 0
        self.caller_id = None
        self.caller_in_wav = None
        self.caller_out_mp3 = None

    @staticmethod
    def hangup_hook(what):
        consoleLog("info", "hangup hook for %s!!\n" % what)
        return

    @staticmethod
    def input_callback(what, obj):
        if what == 'dtmf':
            consoleLog("info", what + " " + obj.digit + "\n")
        else:
            consoleLog("info", what + " " + obj.serialize() + "\n")

    def converTowav(self, filename):
        arr = filename.split('.')
        wavfilename = arr[0] + '.wav'
        fp = open(filename, 'rb')
        data = fp.read()
        fp.close()
        aud = io.BytesIO(data)
        sound = AudioSegment.from_file(aud, format='mp3')
        raw_data = sound._data
        l = len(raw_data)
        f = wave.open(wavfilename, 'wb')
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        f.setnframes(l)
        f.writeframes(raw_data)
        f.close()
        return wavfilename

    def get_voice(self, status=None):
        if not status:
            status = self.status
        filename = '/tmp/%s.mp3' % status
        if os.path.exists(filename):
            return filename
        r = voice_api.bc.tts(self.STATUS_MAP[status], filename)
        if r == 0:
            return filename
        else:
            consoleLog('error', 'baidu tts error: %d' % r['err_no'])
            return None

    def playback_tts_voice(self, text):
        r = voice_api.bc.tts(text, self.caller_out_mp3)
        if r == 0:
            self.session.execute("playback", self.caller_out_mp3)
        else:
            consoleLog('error', 'baidu tts error: %d' % r['err_no'])
            self.session.hangup()

    def playback_status_voice(self, status=None):
        if not status:
            status = self.status
        filename = self.get_voice(status)
        if filename:
            self.session.execute("playback", filename)
        else:
            self.session.hangup()

    def IVR_app(self):
        while self.session.ready():
            print '..........start vad........'
            cmd = "100 400 {0} 4000 10000 100".format(self.caller_in_wav)
            self.session.execute("vad", cmd)
            flag = self.session.getVariable(b"vad_timeout")
            if cmp(flag, 'true') != 0:
                startTime = time.time()
                info = xunfei_asr.vc.getText(self.caller_in_wav)
                endTime = time.time()
                print ("xunfei asr time  : %s " % (endTime - startTime))
                if info['ret'] == 0:
                    input = ''.join(info['result'])
                    print ('xunfei asr result ---%s ' % input)
                    voice_ask = AI_chat.passive_chat(input)
                    self.playback_tts_voice(voice_ask)
                else:
                    voice_ask = AI_chat.passive_chat('')
                    self.playback_tts_voice(voice_ask)
            else:
                self.playback_status_voice('guanzhi_answer_fail')

    def proc_trans_agent(self):
        self.playback_status_voice()
        self.status = 'exit'
        agent_address = 'user/1009'
        self.session.execute("bridge", agent_address)

    def run(self):
        self.session.answer()
        self.caller_id = self.session.getVariable("caller_id_number")
        self.caller_in_wav = '/mnt/%s_in.wav' % self.caller_id
        self.caller_out_mp3 = '/mnt/%s_out.mp3' % self.caller_id
        self.session.setVariable("set_audio_level", "write +2")
        if self.status == 'banks_call':
            filename = self.get_voice()
            self.session.execute("playback", filename)
            self.status = 'trans_bot'
            self.IVR_app()
        elif self.status == 'exit':
            self.session.hangup()


def handler(session, args):
    ivr = IVRBase(session, args)
    ivr.run()
